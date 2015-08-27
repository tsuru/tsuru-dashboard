from django.views.generic import TemplateView
from django.conf import settings

from auth.views import LoginRequiredMixin

import os
import urllib

import requests


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'autoscale/index.html'

    def get_app(self, app_name):
        url = '{}/apps/{}'.format(settings.TSURU_HOST, app_name)
        return requests.get(url, headers=self.authorization).json()

    def get_context_data(self, *args, **kwargs):
        context = super(Index, self).get_context_data(*args, **kwargs)
        token = self.request.session.get('tsuru_token').split(' ')[1]
        token = urllib.quote_plus(token)

        app = self.get_app(kwargs["app"])

        service_url = "{}/app/{}?TSURU_TOKEN={}".format(
            os.environ.get("AUTOSCALE_DASHBOARD_URL"), app["name"], token)

        context["service_url"] = service_url
        context["app"] = app
        return context
