from django.test import TestCase
from django.test.client import RequestFactory

from tsuru_dashboard import settings
from tsuru_dashboard.apps.views import MetricDetail

from mock import patch, Mock


class MetricDetailTest(TestCase):
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
                {"Ip": "10.10.10.10"},
                {"Ip": "9.9.9.9"}
            ],
            "teams": ["tsuruteam", "crane"]
        }
        json_mock = Mock(status_code=200)
        json_mock.json.return_value = self.expected
        requests_mock.return_value = json_mock

        self.response = MetricDetail.as_view()(request, app_name="app1")
        self.request = request

    def test_should_use_detail_template(self):
        self.assertIn("apps/metric_details.html", self.response.template_name)

    @patch('requests.get')
    def test_get_envs(self, get):
        expected = [{"name": "DATABASE_HOST", "value": "localhost", "public": True}]
        response_mock = Mock()
        response_mock.json.return_value = expected
        get.return_value = response_mock

        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}

        view = MetricDetail()
        view.request = request
        envs = view.get_envs("appname")

        self.assertListEqual(envs, expected)
        url = '{}/apps/appname/env'.format(settings.TSURU_HOST)
        get.assert_called_with(url, headers={'authorization': 'admin'})

    def test_should_get_the_app_info_from_tsuru(self):
        self.assertDictEqual(self.expected,
                             self.response.context_data["app"])
