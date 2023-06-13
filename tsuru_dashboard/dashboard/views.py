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

    def get(self, request):
        total_apps, total_containers = self.total_apps_and_containers()

        data = {
            "total_apps": total_apps,
            "total_containers": total_containers,
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
