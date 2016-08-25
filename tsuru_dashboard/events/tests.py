import json
import httpretty
import mock
import base64
import bson

from django.test import TestCase
from django.test.client import RequestFactory

from tsuru_dashboard import settings

from .views import ListEvent, EventInfo, KindList, EventCancel


class ListEventViewTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/?page=2")
        self.request.session = {"tsuru_token": "admin"}

    def mock_kinds(self):
        url = '{}/events/kinds'.format(settings.TSURU_HOST)
        body = json.dumps([{}] * 1000)
        httpretty.register_uri(httpretty.GET, url, body=body, status=200)

    @httpretty.activate
    @mock.patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_should_use_list_template(self, token_is_valid):
        self.mock_kinds()

        token_is_valid.return_value = True

        url = '{}/events'.format(settings.TSURU_HOST)
        body = json.dumps([{
            "EndTime": u'2016-08-05T16:35:28.946-03:00',
            "StartTime": u'2016-08-05T16:35:28.835-03:00'
        }] * 1000)
        httpretty.register_uri(httpretty.GET, url, body=body, status=200)

        response = ListEvent.as_view()(self.request)

        self.assertIn("events/list.html", response.template_name)
        self.assertIn('events', response.context_data.keys())
        self.assertEqual(3, response.context_data["next"])
        self.assertEqual(1, response.context_data["previous"])
        self.assertIn("2", httpretty.last_request().querystring["page"])

    @httpretty.activate
    @mock.patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_kinds(self, token_is_valid):
        self.mock_kinds()

        token_is_valid.return_value = True

        url = '{}/events'.format(settings.TSURU_HOST)
        body = json.dumps([{
            "EndTime": u'2016-08-05T16:35:28.946-03:00',
            "StartTime": u'2016-08-05T16:35:28.835-03:00'
        }] * 1000)
        httpretty.register_uri(httpretty.GET, url, body=body, status=200)

        response = ListEvent.as_view()(self.request)

        self.assertIn('kinds', response.context_data.keys())

    @httpretty.activate
    @mock.patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_should_return_empty_list_when_status_is_204(self, token_is_valid):
        self.mock_kinds()

        token_is_valid.return_value = True

        url = '{}/events'.format(settings.TSURU_HOST)
        httpretty.register_uri(httpretty.GET, url, status=204)

        response = ListEvent.as_view()(self.request)

        self.assertIn("events/list.html", response.template_name)
        self.assertListEqual([], response.context_data['events'])

    @httpretty.activate
    @mock.patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_should_return_empty_kind(self, token_is_valid):
        url = '{}/events/kinds'.format(settings.TSURU_HOST)
        body = json.dumps(range(10000))
        httpretty.register_uri(httpretty.GET, url, body=body, status=204)

        token_is_valid.return_value = True

        url = '{}/events'.format(settings.TSURU_HOST)
        httpretty.register_uri(httpretty.GET, url, status=204)

        response = ListEvent.as_view()(self.request)
        self.assertListEqual([], response.context_data['kinds'])

    @httpretty.activate
    @mock.patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_filter_by_kind(self, token_is_valid):
        self.mock_kinds()

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


class EventInfoViewTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/?page=2")
        self.request.session = {"tsuru_token": "admin"}

    @httpretty.activate
    @mock.patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_event_info(self, token_is_valid):
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

        response = EventInfo.as_view()(self.request, uuid="abc123")

        self.assertIn("events/info.html", response.template_name)
        self.assertIn('event', response.context_data.keys())

    @httpretty.activate
    @mock.patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_event_info_not_found(self, token_is_valid):
        token_is_valid.return_value = True

        event_id = "abc123"
        url = '{}/events/{}'.format(settings.TSURU_HOST, event_id)
        httpretty.register_uri(httpretty.GET, url, status=400)

        response = EventInfo.as_view()(self.request, uuid="abc123")

        self.assertIn("events/info.html", response.template_name)
        self.assertIn('event', response.context_data.keys())


class KindListViewTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/?page=2")
        self.request.session = {"tsuru_token": "admin"}

    def mock_kinds(self):
        url = '{}/events/kinds'.format(settings.TSURU_HOST)
        body = json.dumps([{"Type": "permission", "Name": "app.update.cname.add"}])
        httpretty.register_uri(httpretty.GET, url, body=body, status=200)

    @httpretty.activate
    @mock.patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_view(self, token_is_valid):
        self.mock_kinds()

        response = KindList.as_view()(self.request)
        data = json.loads(response.content)
        self.assertEqual(data[0]["Name"], "app.update.cname.add")


class EventCancelViewTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().post("/", {"reason": "myreason"})
        self.request.session = {"tsuru_token": "admin"}

    @httpretty.activate
    @mock.patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_view(self, token_is_valid):
        url = '{}/events/my-uuid/cancel'.format(settings.TSURU_HOST)
        httpretty.register_uri(httpretty.POST, url, status=204)

        EventCancel.as_view()(self.request, uuid="my-uuid")

        request = httpretty.last_request()
        self.assertEqual("POST", request.method)
        self.assertEqual("/events/my-uuid/cancel", request.path)
        self.assertEqual("reason=myreason", request.body)
