import requests
import json
import re
from dateutil import parser

from pytz import utc

from django.views.generic import TemplateView
from django.conf import settings

from pygments import highlight
from pygments.lexers import DiffLexer
from pygments.formatters import HtmlFormatter

from auth.views import LoginRequiredView

addr_re = re.compile(r"^https?://(.*):\d{1,5}/?")


class ListNode(LoginRequiredView, TemplateView):
    template_name = "docker/list_node.html"

    def units_by_node(self, address):
        address = address.replace("http://", "")
        address = address.split(":")[0]

        url = "{}/docker/node/{}/containers".format(settings.TSURU_HOST, address)
        response = requests.get(url, headers=self.authorization)

        if response.status_code == 204:
            units = []
        else:
            units = response.json() or []

        return len(units)

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

            for node in nodes:
                dt = node["Metadata"].get("LastSuccess")
                node["Metadata"]["LastSuccess"] = self.node_last_success(dt)

                node["Units"] = self.units_by_node(node["Address"])

                pool = node["Metadata"].get("pool")
                nodes_by_pool = pools.get(pool, [])
                nodes_by_pool.append(node)
                pools[pool] = nodes_by_pool

        return pools

    def get_context_data(self, *args, **kwargs):
        context = super(ListNode, self).get_context_data(*args, **kwargs)
        context.update({"pools": self.nodes_by_pool()})
        return context


class ListContainer(LoginRequiredView, TemplateView):
    template_name = "docker/list_container.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ListContainer, self).get_context_data(*args, **kwargs)

        address = kwargs["address"]
        address = address.replace("http://", "")
        address = address.split(":")[0]

        url = "{}/docker/node/{}/containers".format(settings.TSURU_HOST, address)
        response = requests.get(url, headers=self.authorization)

        if response.status_code == 204:
            containers = []
        else:
            containers = response.json()

        context.update({"containers": containers, "address": address})
        return context


class ListDeploy(LoginRequiredView, TemplateView):
    template_name = "deploys/list_deploys.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ListDeploy, self).get_context_data(*args, **kwargs)
        context['services'] = self._get_services(self.request)
        service = self.request.GET.get('service', '')

        page = int(self.request.GET.get('page', '1'))

        skip = (page * 20) - 20
        limit = page * 20

        url = '{}/deploys?service={}&skip={}&limit={}'.format(settings.TSURU_HOST,
                                                              service, skip, limit)

        response = requests.get(url, headers=self.authorization)

        if response.status_code == 204:
            deploys = []
        else:
            deploys = response.json()

        context['deploys'] = deploys
        context['service'] = service

        if len(deploys) >= 20:
            context['next'] = page + 1

        if page > 0:
            context['previous'] = page - 1

        return context

    def _get_services(self, request):
        authorization = {"authorization": request.session.get("tsuru_token")}
        response = requests.get("%s/services/instances" % settings.TSURU_HOST,
                                headers=authorization)
        services = response.json()
        return [s["service"] for s in services if s.get("service")]


class DeploysGraph(LoginRequiredView, TemplateView):
    template_name = "deploys/deploys_graph.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DeploysGraph, self).get_context_data(*args, **kwargs)
        response = requests.get(
            "{}/deploys".format(settings.TSURU_HOST), headers=self.authorization)

        if response.status_code == 204:
            deploys = []
        else:
            deploys = response.json()

        appFilter = self.request.GET.get('app', None)
        appExclude = self.request.GET.get('appExclude', None)
        minTime = self.request.GET.get('minTime', None)
        maxTime = self.request.GET.get('maxTime', None)

        deploysByApp = {}
        for deploy in reversed(deploys):
            if deploy["Duration"] == 0:
                continue

            minutes = deploy["Duration"] / (1000 * 1000 * 1000.0 * 60)
            appName = deploy["App"]

            if appFilter and not re.search(appFilter, appName):
                continue
            if appExclude and re.search(appExclude, appName):
                continue
            if minTime and minutes < int(minTime):
                continue
            if maxTime and minutes > int(maxTime):
                continue

            appEntry = deploysByApp.get(appName)
            if appEntry is None:
                appEntry = {}
                appEntry["key"] = appName
                deploysByApp[appName] = appEntry
            values = appEntry.get("values", [])
            values.append({
                "x": deploy["Timestamp"],
                "y": minutes,
            })
            appEntry["values"] = values

        context['deploys'] = json.dumps([app for app in deploysByApp.values()])
        return context


class DeployInfo(LoginRequiredView, TemplateView):
    template_name = "deploys/deploy_details.html"

    def get_context_data(self, *args, **kwargs):
        deploy_id = kwargs["deploy"]
        url = "{}/deploys/{}".format(settings.TSURU_HOST, deploy_id)
        response = requests.get(url, headers=self.authorization)
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
        events = response.json() or []
        formatted_events = []

        for event in events:
            event['FailingContainer']['ID'] = event['FailingContainer']['ID'][:12]
            event['CreatedContainer']['ID'] = event['CreatedContainer']['ID'][:12]
            event['App'] = event['FailingContainer']['AppName']
            formatted_events.append(event)

        context.update({"events": formatted_events})
        return context
