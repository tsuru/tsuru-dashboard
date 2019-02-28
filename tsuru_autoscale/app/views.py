from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from tsuru_autoscale.instance import client
from tsuru_autoscale.wizard import client as wclient
from tsuru_dashboard.auth.views import LoginRequiredView

import urllib


class AutoScale(LoginRequiredView, TemplateView):
    template_name = 'app/index.html'

    def get(self, request, *args, **kwargs):
        app = kwargs['app']

        token = request.session.get('tsuru_token').split(" ")[-1]
        instances = client.list(token)
        if instances:
            instances = instances.json()
        else:
            instances = []

        instance = None
        auto_scale = None
        events = None

        for inst in instances:
            if app in inst.get('Apps', []):
                instance = inst

                response = wclient.get(instance["Name"], token)
                if response.status_code == 200:
                    auto_scale = response.json()
                    events = wclient.events(instance["Name"], token).json()

        context = {
            "instance": instance,
            "auto_scale": auto_scale,
            "app": app,
            "events": events,
        }
        
        return TemplateResponse(request, self.template_name, context)
