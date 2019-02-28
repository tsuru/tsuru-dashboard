from django.template.response import TemplateResponse

from tsuru_dashboard.auth.views import LoginRequiredView, LoginRequiredMixin
from tsuru_autoscale.instance import client
from tsuru_autoscale.event import client as eclient

class ListInstance(LoginRequiredView):
    template_name = 'instance/list.html'

    def get(self, request, *args, **kwargs):
        token = request.session.get('tsuru_token').split(" ")[-1]
        instances = client.list(token).json()
        context = {
            "list": instances,
        }
        return TemplateResponse(request, self.template_name, context=context)


class InstanceInfo(LoginRequiredView):
    template_name = 'instance/get.html'

    def get(self, request, *args, **kwargs):
        name = kwargs['name']
        token = request.session.get('tsuru_token').split(" ")[-1]
        instance = client.get(name, token).json()
        alarms = client.alarms_by_instance(name, token).json() or []

        events = []

        for alarm in alarms:
            events.extend(eclient.list(alarm["name"], token).json())

        context = {
            "item": instance,
            "alarms": alarms,
            "events": events,
        }
        
        return TemplateResponse(request, self.template_name, context=context)