from django.views.generic import TemplateView

from tsuru_autoscale.auth.views import LoginRequiredView

class ListInstance(LoginRequiredView, TemplateView):
    template_name = 'instance/list.html'

    def get_context_data(self, **kwargs):
        instances = self.client.instance.list().json()
        context = {
            "list": instances,
        }
        return context


class InstanceInfo(LoginRequiredView, TemplateView):
    template_name = 'instance/get.html'

    def get_context_data(self, **kwargs):
        name = kwargs['name']
        instance = self.client.instance.get(name).json()
        alarms = self.client.instance.alarms_by_instance(name).json() or []

        events = []

        for alarm in alarms:
            events.extend(self.client.event.list(alarm["name"]).json())

        context = {
            "item": instance,
            "alarms": alarms,
            "events": events,
        }
        
        return context