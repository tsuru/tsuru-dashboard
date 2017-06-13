from django.test import TestCase
from django.test.client import RequestFactory
from django.http import Http404

from tsuru_dashboard.apps.views import Settings

from mock import patch, Mock


class AppSettingsTestCase(TestCase):
    @patch("requests.get")
    def setUp(self, requests_mock):
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}
        self.expected = {
            "name": "app1",
            "framework": "php",
            "repository": "git@git.com:php.git",
            "state": "dead",
            "units": [
                {"Ip": "10.10.10.10", "Status": "started", "ProcessName": "web"},
                {"Ip": "9.9.9.9", "Status": "stopped", "ProcessName": "worker"},
            ],
            "tags": ["tag 1", "tag 2"],
            "teams": ["tsuruteam", "crane"]
        }
        json_mock = Mock(status_code=200)
        json_mock.json.return_value = self.expected
        requests_mock.return_value = json_mock

        self.response = Settings.as_view()(request, app_name="app1")
        self.request = request

    def test_should_use_settings_template(self):
        self.assertIn("apps/settings.html", self.response.template_name)

    def test_should_get_the_app_info_from_tsuru(self):
        self.assertDictEqual(self.expected, self.response.context_data["app"])

    @patch("requests.get")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_not_found(self, token_is_valid, requests_mock):
        token_is_valid.return_value = True
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}
        requests_mock.return_value = Mock(status_code=404)

        with self.assertRaises(Http404):
            Settings.as_view()(request, app_name="app1")

    @patch("requests.get")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_app_tags(self, token_is_valid, requests_mock):
        token_is_valid.return_value = True
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}
        response_mock = Mock(status_code=200)
        requests_mock.return_value = response_mock

        # Empty string
        response_mock.json.return_value = {"tags": ""}
        response = Settings.as_view()(request, app_name="app1")
        self.assertEqual("", response.context_data["app"]["tags"])

        # Empty array
        response_mock.json.return_value = {"tags": []}
        response = Settings.as_view()(request, app_name="app1")
        self.assertEqual("", response.context_data["app"]["tags"])

        # None
        response_mock.json.return_value = {"tags": None}
        response = Settings.as_view()(request, app_name="app1")
        self.assertEqual("", response.context_data["app"]["tags"])

        # Valid tags
        response_mock.json.return_value = {"tags": ["tag1", "tag2"]}
        response = Settings.as_view()(request, app_name="app1")
        self.assertEqual("tag1, tag2", response.context_data["app"]["tags"])
