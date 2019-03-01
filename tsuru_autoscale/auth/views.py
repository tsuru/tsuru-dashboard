import json
import requests

from tsuru_autoscale import settings
from tsuru_autoscale.client import client
from tsuru_dashboard.auth import views as dashboard_views
from django.utils.decorators import method_decorator

class LoginRequiredView(dashboard_views.LoginRequiredView):

    @property
    def client(self):
        target = settings.AUTOSCALE_HOST
        token = self.request.session.get('tsuru_token').split(" ")[-1]
        return client.Client(target, token)
