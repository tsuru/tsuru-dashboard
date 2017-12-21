from mock import patch, Mock

import httpretty
import json

from django.test import TestCase
from django.test.client import RequestFactory

from tsuru_dashboard import settings
from tsuru_dashboard.apps.views import EventList


class EventListViewTest(TestCase):
    @patch('requests.get')
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def setUp(self, token_is_valid, get):
        token_is_valid.return_value = True
        self.request = RequestFactory().get("/?page=2")
        self.request.session = {"tsuru_token": "admin"}
        self.response = EventList.as_view()(self.request, app_name="appname")

    def test_context_should_contain_app(self):
        self.assertIn('app', self.response.context_data.keys())

    @patch('requests.get')
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_template(self, token_is_valid, get):
        token_is_valid.return_value = True
        get.return_value = Mock(status_code=200)
        self.assertIn("apps/events.html", self.response.template_name)
        self.assertIn('events', self.response.context_data)

    @patch('requests.get')
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_event_list(self, token_is_valid, get):
        token_is_valid.return_value = True
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}

        view = EventList
        view.get_app = Mock()
        self.response = view.as_view()(self.request, app_name="appname")

        url = "{}/events?skip=0&limit=20&target.type=app&target.value=appname"
        url = url.format(settings.TSURU_HOST)
        headers = {'authorization': 'admin'}
        get.assert_called_with(url, headers=headers)

    @patch('requests.get')
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_empty_list(self, token_is_valid, get):
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = None
        get.return_value = response_mock
        token_is_valid.return_value = True

        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}

        view = EventList
        view.get_app = Mock()
        view.as_view()(request, app_name="appname")

        url = '{}/events?skip=0&limit=20&target.type=app&target.value=appname'
        url = url.format(settings.TSURU_HOST)
        headers = {'authorization': 'admin'}
        get.assert_called_with(url, headers=headers)

    @httpretty.activate
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_pagination_page1(self, token_is_valid):
        token_is_valid.return_value = True

        url = '{}/events'.format(settings.TSURU_HOST)
        body = json.dumps([{
            "EndTime": u'2016-08-05T16:35:28.946-03:00',
            "StartTime": u'2016-08-05T16:35:28.835-03:00'
        }] * 1000)
        httpretty.register_uri(httpretty.GET, url, body=body, status=200)

        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}

        response = EventList.as_view()(self.request, app_name="bla")

        self.assertEqual("page=2", response.context_data["next"])
        self.assertEqual(None, response.context_data.get("previous"))

    @httpretty.activate
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_pagination_page2(self, token_is_valid):
        token_is_valid.return_value = True

        url = '{}/events'.format(settings.TSURU_HOST)
        body = json.dumps([{
            "EndTime": u'2016-08-05T16:35:28.946-03:00',
            "StartTime": u'2016-08-05T16:35:28.835-03:00'
        }] * 1000)
        httpretty.register_uri(httpretty.GET, url, body=body, status=200)

        response = EventList.as_view()(self.request, app_name="bla")

        self.assertEqual("page=3", response.context_data["next"])
        self.assertEqual("", response.context_data["previous"])

    @httpretty.activate
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_pagination_page3(self, token_is_valid):
        token_is_valid.return_value = True

        url = '{}/events'.format(settings.TSURU_HOST)
        body = json.dumps([{
            "EndTime": u'2016-08-05T16:35:28.946-03:00',
            "StartTime": u'2016-08-05T16:35:28.835-03:00'
        }] * 1000)
        httpretty.register_uri(httpretty.GET, url, body=body, status=200)

        self.request = RequestFactory().get("/?page=3")
        self.request.session = {"tsuru_token": "admin"}

        response = EventList.as_view()(self.request, app_name="bla")

        self.assertEqual("page=4", response.context_data["next"])
        self.assertEqual("page=2", response.context_data["previous"])
