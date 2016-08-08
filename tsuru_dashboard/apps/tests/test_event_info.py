import json
import httpretty
import mock
import base64
import bson

from django.test import TestCase
from django.test.client import RequestFactory

from tsuru_dashboard import settings

from tsuru_dashboard.apps.views import EventInfo


class EventInfoViewTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/?page=2")
        self.request.session = {"tsuru_token": "admin"}
        self.app_name = "appname"

    @httpretty.activate
    @mock.patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_event_info(self, token_is_valid):
        url = '{}/apps/{}'.format(settings.TSURU_HOST, self.app_name)
        httpretty.register_uri(httpretty.GET, url, body="{}", status=200)
        token_is_valid.return_value = True

        event_id = "abc123"
        url = '{}/events/{}'.format(settings.TSURU_HOST, event_id)
        body = json.dumps({
            "StartCustomData": {
                "Data": base64.b64encode(bson.BSON.encode({"start": 1}))
            },
            "EndCustomData": {
                "Data": base64.b64encode(bson.BSON.encode({"end": 1}))
            },
            "OtherCustomData": {
                "Data": base64.b64encode(bson.BSON.encode({"other": 1}))
            }
        })
        httpretty.register_uri(httpretty.GET, url, body=body, status=200)

        response = EventInfo.as_view()(self.request, uuid="abc123", app_name=self.app_name)

        self.assertIn("apps/event.html", response.template_name)
        self.assertIn('event', response.context_data.keys())

    @httpretty.activate
    @mock.patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_event_info_not_found(self, token_is_valid):
        url = '{}/apps/{}'.format(settings.TSURU_HOST, self.app_name)
        httpretty.register_uri(httpretty.GET, url, body="{}", status=200)
        token_is_valid.return_value = True

        event_id = "abc123"
        url = '{}/events/{}'.format(settings.TSURU_HOST, event_id)
        httpretty.register_uri(httpretty.GET, url, status=400)

        response = EventInfo.as_view()(self.request, uuid="abc123", app_name=self.app_name)

        self.assertIn("apps/event.html", response.template_name)
        self.assertIn('event', response.context_data.keys())
