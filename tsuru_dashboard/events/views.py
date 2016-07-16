import requests

from django.views.generic import TemplateView

from tsuru_dashboard import settings
from tsuru_dashboard.auth.views import LoginRequiredView


class ListEvent(LoginRequiredView, TemplateView):
    template_name = "events/list.html"

    def get_events(self):
        url = '{}/events'.format(settings.TSURU_HOST)
        response = requests.get(
            url, headers=self.authorization, params=self.request.GET)

        if response.status_code == 204:
            return []

        return response.json()

    def get_kinds(self):
        url = '{}/events/kinds'.format(settings.TSURU_HOST)
        response = requests.get(
            url, headers=self.authorization, params=self.request.GET)

        if response.status_code == 204:
            return []

        return response.json()

    def get_context_data(self, *args, **kwargs):
        context = super(ListEvent, self).get_context_data(*args, **kwargs)
        context['events'] = self.get_events()
        context['kinds'] = self.get_kinds()
        return context


class EventInfo(LoginRequiredView, TemplateView):
    template_name = "events/info.html"

    def get_event(self, uuid):
        url = '{}/events/{}'.format(settings.TSURU_HOST, uuid)
        response = requests.get(
            url, headers=self.authorization, params=self.request.GET)

        if response.status_code == 200:
            return response.json()
        return None

    def get_context_data(self, *args, **kwargs):
        context = super(EventInfo, self).get_context_data(*args, **kwargs)
        context['event'] = self.get_event(kwargs["uuid"])
        return context
