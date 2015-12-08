import requests

from datetime import datetime, timedelta

from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import TemplateView

from pytz import utc
from dateutil import parser

from tsuru_dashboard import settings
from tsuru_dashboard.auth.views import LoginRequiredView


class DashboardView(LoginRequiredView, TemplateView):
    template_name = "dashboard/dashboard.html"


class HealingView(LoginRequiredView):
    def get(self, request):
        url = "{}/docker/healing".format(settings.TSURU_HOST)
        response = requests.get(url, headers=self.authorization)

        if response.status_code != 200:
            return JsonResponse({"healing": 0})

        healings = 0
        for healing in response.json():
            end_time = parser.parse(healing['EndTime'])
            if end_time.tzinfo:
                end_time = end_time.astimezone(utc)
            else:
                end_time = utc.localize(end_time)
            now = utc.localize(datetime.utcnow())
            if (now - end_time < timedelta(days=1)):
                healings += 1
        return JsonResponse({"healing": healings}, safe=False)


class CloudStatusView(LoginRequiredView):
    def total_apps_and_containers(self):
        url = "{}/apps".format(settings.TSURU_HOST)
        response = requests.get(url, headers=self.authorization)
        total_containers = 0

        if response.status_code != 200:
            return 0, total_containers

        apps = response.json()
        for app in apps:
            total_containers += len(app['units'])

        return len(apps), total_containers

    def total_nodes(self):
        url = "{}/docker/node".format(settings.TSURU_HOST)
        response = requests.get(url, headers=self.authorization)

        if response.status_code != 200:
            return 0

        nodes = response.json()
        return len(nodes['nodes'])

    def containers_by_nodes(self, containers, nodes):
        if containers <= 0 or nodes <= 0:
            return 0
        return containers/nodes

    def get(self, request):
        total_apps, total_containers = self.total_apps_and_containers()
        total_nodes = self.total_nodes()
        containers_by_nodes = self.containers_by_nodes(total_containers, total_nodes)

        data = {
            "total_apps": total_apps,
            "containers_by_nodes": containers_by_nodes,
            "total_containers": total_containers,
            "total_nodes": total_nodes,
        }
        return JsonResponse(data, safe=False)


class DeploysView(LoginRequiredView):
    def get(self, request):
        url = "{}/deploys?limit=1000".format(settings.TSURU_HOST)
        deploys = requests.get(url, headers=self.authorization).json() or []
        errored = 0
        last_deploys = 0
        for deploy in deploys:
            timestamp = parser.parse(deploy['Timestamp'])
            if timestamp.tzinfo:
                timestamp = timestamp.astimezone(utc)
            else:
                timestamp = utc.localize(timestamp)
            now = utc.localize(datetime.utcnow())
            if (now - timestamp < timedelta(days=1)):
                if deploy['Error']:
                    errored += 1
                last_deploys += 1
        return JsonResponse({"last_deploys": last_deploys, "errored": errored}, safe=False)


class IndexView(LoginRequiredView):
    def get(self, request):
        return HttpResponseRedirect("/apps")
