import requests
import re

from datetime import datetime, timedelta

from dateutil import parser
from django.template.response import TemplateResponse
from django.views.generic import View
from django.conf import settings
from django.http import JsonResponse
from pytz import utc

from auth.views import LoginRequiredView


class DashboardView(LoginRequiredView):
    def get(self, request):
        return TemplateResponse(request, 'dashboard/dashboard.html')


class HealingView(LoginRequiredView):
    def get(self, request):
        authorization = {"authorization": request.session.get("tsuru_token")}
        url = "{}/docker/healing".format(settings.TSURU_HOST)
        resp = requests.get(url, headers=authorization).json() or []
        healings = 0
        for healing in resp:
            end_time = healing['EndTime']
            try:
                end_time = parser.parse(end_time)
                if not end_time.tzinfo:
                    end_time = utc.localize(end_time)
                else:
                    end_time = end_time.astimezone(utc)
                now = utc.localize(datetime.utcnow())
                if (now - end_time < timedelta(days=1)):
                    healings += 1
            except ValueError:
                pass
        return JsonResponse({"healing": healings}, safe=False)


class CloudStatusView(View):
    def get(self, request):
        authorization = {"authorization": request.session.get("tsuru_token")}
        url = "{}/apps".format(settings.TSURU_HOST)
        apps = requests.get(url, headers=authorization).json()
        total_containers = 0
        for app in apps:
            total_containers += len(app['units'])
        url = "{}/docker/node".format(settings.TSURU_HOST)
        nodes = requests.get(url, headers=authorization).json()
        data = {
            "total_apps": len(apps),
            "containers_by_nodes": total_containers/len(nodes['nodes']),
            "total_containers": total_containers,
            "total_nodes": len(nodes['nodes'])
        }
        return JsonResponse(data, safe=False)


class DeploysView(View):
    def get(self, request):
        authorization = {"authorization": request.session.get("tsuru_token")}
        url = "{}/deploys?limit=250".format(settings.TSURU_HOST)
        deploys = requests.get(url, headers=authorization).json()
        errored = 0
        last_deploys = 0
        for deploy in deploys:
            timestamp = deploy['Timestamp']
            formated_timestamp = re.split("\.\d{0,5}", timestamp)
            formated_timestamp = "".join(formated_timestamp)
            timestamp = parser.parse(formated_timestamp)
            if (datetime.now() - timestamp < timedelta(days=1)):
                if deploy['Error']:
                    errored += 1
                last_deploys += 1
        return JsonResponse({"last_deploys": last_deploys, "errored": errored}, safe=False)
