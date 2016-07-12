import json
import httpretty
import mock

from django.test import TestCase
from django.test.client import RequestFactory

from tsuru_dashboard import settings

from .views import ListEvent


class ListEventViewTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/?page=2")
        self.request.session = {"tsuru_token": "admin"}

    @httpretty.activate
    @mock.patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_should_use_list_template(self, token_is_valid):
        token_is_valid.return_value = True

        url = '{}/events'.format(settings.TSURU_HOST)
        body = json.dumps(range(10000))
        httpretty.register_uri(httpretty.GET, url, body=body, status=200)

        response = ListEvent.as_view()(self.request)

        self.assertIn("events/list.html", response.template_name)
        self.assertIn('events', response.context_data.keys())

    @httpretty.activate
    @mock.patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_should_return_empty_list_when_status_is_204(self, token_is_valid):
        token_is_valid.return_value = True

        url = '{}/events'.format(settings.TSURU_HOST)
        httpretty.register_uri(httpretty.GET, url, status=204)

        response = ListEvent.as_view()(self.request)

        self.assertIn("events/list.html", response.template_name)
        self.assertListEqual([], response.context_data['events'])

    @httpretty.activate
    @mock.patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_filter_by_kind(self, token_is_valid):
        token_is_valid.return_value = True

        url = '{}/events?kind='.format(settings.TSURU_HOST)

        def body(request, uri, headers):
            events = []
            if request.querystring.get("kindName", [""])[0] != "nothing":
                events = [{"kind": "some"}]
            return (200, headers, json.dumps(events))

        httpretty.register_uri(httpretty.GET, url, body=body, status=200)

        request = RequestFactory().get("")
        request.session = {"tsuru_token": "admin"}
        response = ListEvent.as_view()(request)
        self.assertEqual(len(response.context_data['events']), 1)

        request = RequestFactory().get("?kindName=nothing")
        request.session = {"tsuru_token": "admin"}
        response = ListEvent.as_view()(request)
        self.assertEqual(len(response.context_data['events']), 0)
