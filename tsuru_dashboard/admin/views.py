import requests
import grequests
import json
from urlparse import urlparse
from dateutil import parser

from django.views.generic import TemplateView
from django.http import HttpResponse, Http404, JsonResponse, StreamingHttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib import messages

from pygments import highlight
from pygments.lexers import DiffLexer
from pygments.formatters import HtmlFormatter
from pytz import utc

from tsuru_dashboard import settings
from tsuru_dashboard.auth.views import LoginRequiredView


class PoolList(LoginRequiredView, TemplateView):
    template_name = "admin/pool_list.html"

    def extract_ip(self, address):
        if not urlparse(address).scheme:
            address = "http://"+address
        return urlparse(address).hostname

    def get_node(self, address, data):
        for response in data:
            if response.status_code != 200:
                continue

            node_units = response.json()
            if not node_units:
                continue

            if 'HostAddr' not in node_units[0]:
                continue

            if self.extract_ip(node_units[0]['HostAddr']) == self.extract_ip(address):
                return node_units
        return []

    def units_by_node(self, address, units):
        units = self.get_node(address, units)
        result = {}

        for unit in units:
            if not unit['Status'] in result:
                result[unit['Status']] = 0

            result[unit['Status']] += 1

        len_units = len(units)
        if len_units > 0:
            result['total'] = len_units

        return result

    def node_last_success(self, date):
        if date:
            last_success = parser.parse(date)
            if last_success.tzinfo:
                last_success = last_success.astimezone(utc)
            else:
                last_success = utc.localize(last_success)
            return last_success
        return date

    def nodes_by_pool(self):
        url = "{}/docker/node".format(settings.TSURU_HOST)
        response = requests.get(url, headers=self.authorization)
        pools = {}

        if response.status_code != 204:
            data = response.json()
            nodes = data.get("nodes", [])

            url = "{}/docker/node/{}/containers"
            urls = [url.format(settings.TSURU_HOST, node["Address"]) for node in nodes]

            rs = (grequests.get(u, headers=self.authorization) for u in urls)
            units = grequests.map(rs)

            for node in nodes:
                dt = node["Metadata"].get("LastSuccess")
                node["Metadata"]["LastSuccess"] = self.node_last_success(dt)
                node["Units"] = self.units_by_node(node["Address"], units)
                pool = node["Metadata"].get("pool")
                nodes_by_pool = pools.get(pool, [])
                nodes_by_pool.append(node)
                pools[pool] = nodes_by_pool
        return sorted(pools.items())

    def get_context_data(self, *args, **kwargs):
        context = super(PoolList, self).get_context_data(*args, **kwargs)
        context.update({"pools": self.nodes_by_pool()})
        return context


class NodeInfo(LoginRequiredView, TemplateView):
    template_name = "admin/node_info.html"


class NodeInfoJson(LoginRequiredView):
    def get_containers(self, node_address):
        url = "{}/docker/node/{}/containers".format(settings.TSURU_HOST, node_address)
        response = requests.get(url, headers=self.authorization)

        if response.status_code == 204:
            return []

        if response.status_code > 399:
            return []

        return response.json() or []

    def get_node(self, address):
        url = "{}/docker/node".format(settings.TSURU_HOST)
        response = requests.get(url, headers=self.authorization)

        if response.status_code != 204:
            data = response.json()
            nodes = data.get("nodes", [])

            for node in nodes:
                if node["Address"] == address:
                    return node

        return None

    def get(self, *args, **kwargs):
        containers = self.get_containers(kwargs["address"])
        for container in containers:
            if "AppName" in container:
                container["DashboardURL"] = reverse(
                    'detail-app', kwargs={'app_name': container["AppName"]})
        return JsonResponse({
            "node": {
                "info": self.get_node(kwargs["address"]),
                "containers": containers,
                "nodeRemovalURL": reverse('node-remove', kwargs={'address': kwargs["address"]})
            }
        })


class ListDeploy(LoginRequiredView, TemplateView):
    template_name = "deploys/list_deploys.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ListDeploy, self).get_context_data(*args, **kwargs)

        page = int(self.request.GET.get('page', '1'))

        skip = (page * 20) - 20
        limit = page * 20

        url = '{}/deploys?skip={}&limit={}'.format(settings.TSURU_HOST, skip, limit)

        response = requests.get(url, headers=self.authorization)

        if response.status_code == 204:
            deploys = []
        else:
            deploys = response.json()

        context['deploys'] = deploys

        if len(deploys) >= 20:
            context['next'] = page + 1

        if page > 0:
            context['previous'] = page - 1

        return context


class DeployInfo(LoginRequiredView, TemplateView):
    template_name = "deploys/deploy_details.html"

    def get_context_data(self, *args, **kwargs):
        deploy_id = kwargs["deploy"]

        url = "{}/deploys/{}".format(settings.TSURU_HOST, deploy_id)
        response = requests.get(url, headers=self.authorization)

        if response.status_code > 399:
            raise Http404("Deploy does not exist")

        context = {"deploy": response.json()}

        diff = context["deploy"].get("Diff")
        if diff and diff != u'The deployment must have at least two commits for the diff.':
            format = HtmlFormatter()
            diff = highlight(diff, DiffLexer(), format)
        else:
            diff = None

        context["deploy"]["Diff"] = diff
        return context


class ListHealing(LoginRequiredView, TemplateView):
    template_name = "docker/list_healing.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ListHealing, self).get_context_data(*args, **kwargs)
        url = '{}/docker/healing'.format(settings.TSURU_HOST)
        response = requests.get(url, headers=self.authorization)
        formatted_events = []
        if response.status_code == 200:
            events = response.json() or []
            formatted_events = []

            for event in events:
                event['FailingContainer']['ID'] = event['FailingContainer']['ID'][:12]
                event['CreatedContainer']['ID'] = event['CreatedContainer']['ID'][:12]
                event['App'] = event['FailingContainer']['AppName']
                formatted_events.append(event)

        context.update({"events": formatted_events})
        return context


class PoolInfo(LoginRequiredView, TemplateView):
    template_name = "docker/pool_info.html"

    def get_node(self, address, data):
        for response in data:
            if response.status_code != 200:
                continue

            node_units = response.json()
            if not node_units:
                continue

            if 'HostAddr' not in node_units[0]:
                continue

            if node_units[0]['HostAddr'] in address:
                return node_units
        return []

    def units_by_node(self, address, units):
        units = self.get_node(address, units)
        result = {}

        for unit in units:
            if not unit['Status'] in result:
                result[unit['Status']] = 0

            result[unit['Status']] += 1

        len_units = len(units)
        if len_units > 0:
            result['total'] = len_units

        return result

    def node_last_success(self, date):
        if date:
            last_success = parser.parse(date)
            if last_success.tzinfo:
                last_success = last_success.astimezone(utc)
            else:
                last_success = utc.localize(last_success)
            return last_success
        return date

    def nodes_by_pool(self, pool):
        url = "{}/docker/node".format(settings.TSURU_HOST)
        response = requests.get(url, headers=self.authorization)
        pools = {}

        if response.status_code != 204:
            data = response.json()
            nodes = data.get("nodes", [])

            url = "{}/docker/node/{}/containers"
            urls = [url.format(settings.TSURU_HOST, node["Address"]) for node in nodes]

            rs = (grequests.get(u, headers=self.authorization) for u in urls)
            units = grequests.map(rs)

            for node in nodes:
                if node["Metadata"].get("pool", "") != pool:
                    continue

                dt = node["Metadata"].get("LastSuccess")
                node["Metadata"]["LastSuccess"] = self.node_last_success(dt)

                node["Units"] = self.units_by_node(node["Address"], units)

                pool = node["Metadata"].get("pool")
                nodes_by_pool = pools.get(pool, [])
                nodes_by_pool.append(node)
                pools[pool] = nodes_by_pool

        return pools

    def get_context_data(self, *args, **kwargs):
        context = super(PoolInfo, self).get_context_data(*args, **kwargs)
        context.update({"pools": self.nodes_by_pool(kwargs["pool"])})
        return context


class NodeRemove(LoginRequiredView):
    def get(self, request, *args, **kwargs):
        address = self.kwargs['address']

        msg = u"The value for '{}' parameter should be 'true' or 'false'"

        destroy = self.request.GET.get("destroy", "false")
        if destroy not in ["true", "false"]:
            return HttpResponse(msg.format("destroy"), status=400)

        rebalance = self.request.GET.get("rebalance", "false")
        if rebalance not in ["true", "false"]:
            return HttpResponse(msg.format("rebalance"), status=400)
        no_rebalance = "false" if rebalance == "true" else "true"

        response = requests.delete(
            '{}/docker/node/{}?remove-iaas={}&no-rebalance={}'.format(
                settings.TSURU_HOST, address, destroy, no_rebalance
            ),
            headers=self.authorization
        )

        if response.status_code > 399:
            return HttpResponse(response.text, status=response.status_code)

        return redirect(reverse('pool-list'))


class TemplateListJson(LoginRequiredView):

    def get(self, *args, **kwargs):
        templates = self.client.templates.list()
        return JsonResponse(templates, safe=False)


class NodeAdd(LoginRequiredView):

    def post(self, *args, **kwargs):
        resp = self.client.nodes.create(**self.request.POST.dict())

        for line in resp.iter_lines():
            msg_err = json.loads(line).get('Error')
            if msg_err:
                messages.error(self.request, msg_err, fail_silently=True)
                return HttpResponse(msg_err, status=500)

        messages.success(self.request, u'Node was successfully created', fail_silently=True)
        return HttpResponse('Node was successfully created', status=200)


class PoolRebalance(LoginRequiredView):

    def post(self, *args, **kwargs):
        def sending_stream():
            r = self.client.pools.rebalance(pool=kwargs["pool"])
            for line in r.iter_lines():
                yield "{}<br>".format(line)
        return StreamingHttpResponse(sending_stream())
