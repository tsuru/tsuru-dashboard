from django.http import HttpResponse
from django.conf import settings

from auth.views import LoginRequiredView

import json
import requests


class Metric(LoginRequiredView):
    @property
    def authorization(self):
        return {'authorization': self.request.session.get('tsuru_token')}

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
        from metrics.backend import get_backend
        app_name = kwargs['app_name']
        app = self.get_app(app_name)
        app["envs"] = self.get_envs(self.request, app_name)

        backend = get_backend(app)
        data = backend.cpu_max()
        return HttpResponse(json.dumps(data))
