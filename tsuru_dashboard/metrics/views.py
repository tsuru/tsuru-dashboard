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

    def get_metrics_backend(self, target_name, target_type, token, date_range):
        from .backend import get_backend
        if target_type == "component":
            return get_backend(app=None, component_name=target_name, token=token, date_range=date_range)
        elif target_type == "app":
            app = self.get_app(target_name)
            app["envs"] = self.get_envs(self.request, target_name)
            process_name = self.request.GET.get("process_name")
            return get_backend(
                app=app,
                token=token,
                date_range=date_range,
                process_name=process_name
            )
        return None

    def get(self, *args, **kwargs):
        token = self.request.session.get('tsuru_token')
        metric = self.request.GET.get("metric")
        if not metric:
            return HttpResponseBadRequest()

        interval = self.request.GET.get("interval")
        date_range = self.request.GET.get("date_range")
        target_name = kwargs['target_name']
        target_type = kwargs['target_type']

        backend = self.get_metrics_backend(
            target_name=target_name, target_type=target_type, token=token, date_range=date_range)
        if backend is None:
            return HttpResponseBadRequest()

        data = getattr(backend, metric)(interval=interval)
        return HttpResponse(json.dumps(data))
