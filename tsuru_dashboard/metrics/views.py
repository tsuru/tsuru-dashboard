from django.http import HttpResponse, HttpResponseBadRequest

from tsuru_dashboard import settings
from tsuru_dashboard.auth.views import LoginRequiredView

import json
import requests


class Metric(LoginRequiredView):
    def get_app(self, app_name):
        url = '{}/apps/{}'.format(settings.TSURU_HOST, app_name)
        return requests.get(url, headers=self.authorization).json()

    def get_envs(self, request, app_name):
        url = '{}/apps/{}/env'.format(settings.TSURU_HOST, app_name)
        data = requests.get(url, headers=self.authorization).json()
        envs = {}

        for env in data:
            envs[env['name']] = env['value']

        return envs

    def get(self, *args, **kwargs):
        metric = self.request.GET.get("metric")
        if not metric:
            return HttpResponseBadRequest()

        process_name = self.request.GET.get("process_name")

        app_name = kwargs['app_name']
        app = self.get_app(app_name)
        app["envs"] = self.get_envs(self.request, app_name)

        from .backend import get_backend
        token = self.request.session.get('tsuru_token')
        backend = get_backend(app, token)

        interval = self.request.GET.get("interval")
        date_range = self.request.GET.get("date_range")
        data = getattr(backend, metric)(date_range=date_range, interval=interval, process_name=process_name)
        return HttpResponse(json.dumps(data))
