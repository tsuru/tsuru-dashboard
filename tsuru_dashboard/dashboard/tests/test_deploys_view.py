import json

from django.test import TestCase
from django.test.client import RequestFactory
from freezegun import freeze_time
from mock import Mock, patch

from tsuru_dashboard.auth.views import LoginRequiredView
from tsuru_dashboard.dashboard.views import DeploysView


class DeploysViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_requires_login(self):
        assert issubclass(DeploysView, LoginRequiredView), \
            "DeploysView should inherit from LoginRequiredView"

    @patch("requests.get")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_get_no_deploys(self, token_is_valid, get):
        token_is_valid.return_value = True
        resp = Mock()
        resp.json.return_value = None
        get.return_value = resp
        request = self.factory.get("/dashboard/deploys")
        request.session = {"tsuru_token": "sometoken"}
        response = DeploysView.as_view()(request)
        self.assertEqual(200, response.status_code)
        result = json.loads(response.content)
        self.assertEqual({"last_deploys": 0, "errored": 0}, result)

    @freeze_time("2012-04-01 16:32:15", tz_offset=0)
    @patch("requests.get")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_get_filtering(self, token_is_valid, get):
        token_is_valid.return_value = True
        resp = Mock()
        resp.json.return_value = [
            {"Timestamp": "2012-03-31T12:10:15Z",
             "Error": "something went wrong"},
            {"Timestamp": "2012-03-31T09:02:15-0300",
             "Error": None},
            {"Timestamp": "2012-04-01T19:02:15+0800",
             "Error": None},
            {"Timestamp": "2012-03-31T00:02:15-0800",
             "Error": None},
            {"Timestamp": "2012-04-01T10:02:15.903-0300",
             "Error": "a failure in the deploy"},
            {"Timestamp": "2012-03-31T13:32:16-0300",
             "Error": None},
            {"Timestamp": "2012-03-31T20:00:00.903Z",
             "Error": None},
            {"Timestamp": "2012-03-31T20:00:00",
             "Error": "deployment failed"},
        ]
        get.return_value = resp
        request = self.factory.get("/dashboard/deploys")
        request.session = {"tsuru_token": "sometoken"}
        response = DeploysView.as_view()(request)
        self.assertEqual(200, response.status_code)
        result = json.loads(response.content)
        self.assertEqual({"last_deploys": 5, "errored": 2}, result)
