import requests
import bson
import base64

import json
import yaml

from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse

from pygments import highlight
from pygments.lexers import YamlLexer
from pygments.formatters import HtmlFormatter

from dateutil import parser

from tsuru_dashboard import settings
from tsuru_dashboard.auth.views import LoginRequiredView


class KindList(LoginRequiredView):

    def get_kinds(self):
        url = '{}/events/kinds'.format(settings.TSURU_HOST)
        response = requests.get(
            url, headers=self.authorization, params=self.request.GET)

        if response.status_code == 204:
            return []

        return response.json()

    def get(self, *args, **kwargs):
        return JsonResponse(self.get_kinds(), safe=False)


class ListEvent(LoginRequiredView, TemplateView):
    template_name = "events/list.html"
    EVENTS_PER_PAGE = 20

    def get_events(self, skip, limit):
        url = '{}/events?skip={}&limit={}'.format(
            settings.TSURU_HOST, skip, limit)
        response = requests.get(
            url, headers=self.authorization, params=self.request.GET)

        if response.status_code == 204:
            return []

        events = response.json()

        for event in events:
            if "StartTime" in event:
                event["StartTime"] = parser.parse(event["StartTime"])
            if "EndTime" in event:
                event["EndTime"] = parser.parse(event["EndTime"])

        return events

    def get_kinds(self):
        url = '{}/events/kinds'.format(settings.TSURU_HOST)
        response = requests.get(
            url, headers=self.authorization, params=self.request.GET)

        if response.status_code == 204:
            return []

        return response.json()

    def get_context_data(self, *args, **kwargs):
        context = super(ListEvent, self).get_context_data(*args, **kwargs)

        page = 1
        try:
            page = int(self.request.GET.get('page', '1'))
        except ValueError:
            pass
        if page < 1:
            page = 1

        skip = (page - 1) * self.EVENTS_PER_PAGE
        limit = self.EVENTS_PER_PAGE

        context['events'] = self.get_events(skip, limit)
        context['kinds'] = self.get_kinds()

        req_copy = self.request.GET.copy()
        if len(context['events']) >= self.EVENTS_PER_PAGE:
            req_copy['page'] = page + 1
            context['next'] = req_copy.urlencode()

        if page > 1:
            req_copy['page'] = page - 1
            if req_copy['page'] == 1:
                del req_copy['page']
            context['previous'] = req_copy.urlencode()

        return context


def event_serialization_default(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    return None


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
                data = json.loads(json.dumps(data, default=event_serialization_default))
                data = yaml.safe_dump(data, default_flow_style=False, default_style='')
                data = highlight(data, YamlLexer(), HtmlFormatter())
                event[field]["Data"] = data

        return event

    def decode_bson(self, data):
        return bson.BSON(base64.b64decode(data["Data"])).decode()

    def get_context_data(self, *args, **kwargs):
        context = super(EventInfo, self).get_context_data(*args, **kwargs)
        context['event'] = self.get_event(kwargs["uuid"])
        return context


class EventCancel(LoginRequiredView):

    def cancel(self, uuid, reason):
        url = '{}/events/{}/cancel'.format(settings.TSURU_HOST, uuid)
        data = {"reason": reason}
        requests.post(url, data=data, headers=self.authorization)

    def post(self, *args, **kwargs):
        uuid = kwargs["uuid"]
        self.cancel(uuid, self.request.POST.get("reason", ""))
        return HttpResponse()
