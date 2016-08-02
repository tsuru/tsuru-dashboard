import requests
import bson
import base64

import json
import yaml
from bson import json_util

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


def event_serialization_default(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    return json_util.default


class EventInfo(LoginRequiredView, TemplateView):
    template_name = "events/info.html"

    def get_event(self, uuid):
        url = '{}/events/{}'.format(settings.TSURU_HOST, uuid)
        response = requests.get(
            url, headers=self.authorization, params=self.request.GET)

        if response.status_code == 200:
            event = response.json()
            return self.decode_custom_data(event)

        return None

    def decode_custom_data(self, event):
        fields = ["StartCustomData", "EndCustomData", "OtherCustomData"]

        for field in fields:
            if event.get(field) and event[field].get("Data"):
                data = self.decode_bson(event[field])
                data = json.loads(json.dumps(
                    data, default=event_serialization_default))
                event[field]["Data"] = yaml.safe_dump(
                    data, default_flow_style=False, default_style='')

        return event

    def decode_bson(self, data):
        return bson.BSON(base64.b64decode(data["Data"])).decode()

    def get_context_data(self, *args, **kwargs):
        context = super(EventInfo, self).get_context_data(*args, **kwargs)
        context['event'] = self.get_event(kwargs["uuid"])
        return context
