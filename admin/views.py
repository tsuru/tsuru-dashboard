import requests
import json
import re

from datetime import datetime

from django.template.response import TemplateResponse
from django.conf import settings

from pygments import highlight
from pygments.lexers import DiffLexer
from pygments.formatters import HtmlFormatter

from auth.views import LoginRequiredView

addr_re = re.compile(r"^https?://(.*):\d{1,5}/?")


class ListNode(LoginRequiredView):
    def get(self, request):
        authorization = {'authorization': request.session.get('tsuru_token')}
        response = requests.get('%s/docker/node' % settings.TSURU_HOST,
                                headers=authorization)
        pools = {}
        if response.status_code != 204:
            data = response.json()
            nodes = data.get("nodes", [])

            for node in nodes:
                dt = node["Metadata"].get("LastSuccess", "")
                if dt:
                    node["Metadata"]["LastSuccess"] = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S-03:00")
                nodes_by_pool = pools.get(node["Metadata"].get("pool"), [])
                nodes_by_pool.append(node)
                pools[node["Metadata"].get("pool")] = nodes_by_pool

        return TemplateResponse(request, "docker/list_node.html",
                                {"pools": pools})


class ListContainer(LoginRequiredView):
    def get(self, request, address):
        address = address.replace("http://", "")
        address = address.split(":")[0]
        authorization = {'authorization': request.session.get('tsuru_token')}
        url = '%s/docker/node/%s/containers' % (settings.TSURU_HOST, address)
        response = requests.get(url, headers=authorization)
        if response.status_code == 204:
            containers = []
        else:
            containers = response.json()
        return TemplateResponse(request, "docker/list_container.html",
                                {'containers': containers, 'address': address})


class ListDeploy(LoginRequiredView):
    template = "deploys/list_deploys.html"

    def get(self, request):
        context = {}
        context['services'] = self._get_services(request)
        service = request.GET.get('service', '')

        page = int(request.GET.get('page', '1'))

        skip = (page * 20) - 20
        limit = page * 20

        url = '{}/deploys?service={}&skip={}&limit={}'.format(settings.TSURU_HOST,
                                                              service, skip, limit)

        authorization = {'authorization': request.session.get('tsuru_token')}
        response = requests.get(url, headers=authorization)

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

        return TemplateResponse(request, self.template, context=context)

    def _get_services(self, request):
        authorization = {"authorization": request.session.get("tsuru_token")}
        response = requests.get("%s/services/instances" % settings.TSURU_HOST,
                                headers=authorization)
        services = response.json()
        return [s["service"] for s in services if s.get("service")]


class DeploysGraph(LoginRequiredView):
    template = "deploys/deploys_graph.html"

    def get(self, request):
        context = {}
        authorization = {'authorization': request.session.get('tsuru_token')}
        response = requests.get('%s/deploys' % (settings.TSURU_HOST),
                                headers=authorization)
        if response.status_code == 204:
            deploys = []
        else:
            deploys = response.json()

        appFilter = request.GET.get('app', None)
        appExclude = request.GET.get('appExclude', None)
        minTime = request.GET.get('minTime', None)
        maxTime = request.GET.get('maxTime', None)

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
        return TemplateResponse(request, self.template, context=context)


class DeployInfo(LoginRequiredView):
    def get(self, request, *args, **kwargs):
        deploy_id = kwargs["deploy"]
        headers = {'authorization': request.session.get('tsuru_token')}
        url = "{0}/deploys/{1}".format(settings.TSURU_HOST, deploy_id)
        response = requests.get(url, headers=headers)
        context = {"deploy": response.json()}
        format = HtmlFormatter()
        diff_output = highlight(context["deploy"].get("Diff", ""), DiffLexer(), format)
        context["deploy"]["Diff"] = diff_output
        return TemplateResponse(request, "deploys/deploy_details.html", context)


class ListHealing(LoginRequiredView):
    @property
    def authorization(self):
        return {'authorization': self.request.session.get('tsuru_token')}

    def get(self, request):
        url = '{}/docker/healing'.format(settings.TSURU_HOST)
        response = requests.get(url, headers=self.authorization)
        events = response.json()
        formatted_events = []
        for event in events:
            event['FailingContainer']['ID'] = event['FailingContainer']['ID'][:12]
            event['CreatedContainer']['ID'] = event['CreatedContainer']['ID'][:12]
            event['App'] = event['FailingContainer']['AppName']
            formatted_events.append(event)
        return TemplateResponse(request, "docker/list_healing.html", {"events": formatted_events})
