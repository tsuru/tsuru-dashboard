import requests

from django.views.generic import TemplateView

from tsuru_dashboard import settings
from tsuru_dashboard.auth.views import LoginRequiredView


class ListEvent(LoginRequiredView, TemplateView):
    template_name = "events/list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ListEvent, self).get_context_data(*args, **kwargs)

        url = '{}/events'.format(settings.TSURU_HOST)
        response = requests.get(url, headers=self.authorization)

        if response.status_code == 204:
            events = []
        else:
            events = response.json()

        context['events'] = events
        return context
