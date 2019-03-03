import urllib
from django.views.generic import TemplateView
from tsuru_autoscale.auth.views import LoginRequiredView


class IndexView(LoginRequiredView, TemplateView):
    template_name = 'app/index.html'

    def get_context_data(self, **kwargs):
        app = kwargs['app']

        instances = self.client.instance.list()
        instance = None
        auto_scale = None
        events = None

        for inst in instances:
            if app in inst.get('Apps', []):
                instance = inst

                response = self.client.wizard.get(instance["Name"])
                if response.status_code == 200:
                    auto_scale = response.json()
                    events = self.client.wizard.events(instance["Name"]).json()

        context = {
            "instance": instance,
            "auto_scale": auto_scale,
            "app": app,
            "events": events,
        }
        
        return context