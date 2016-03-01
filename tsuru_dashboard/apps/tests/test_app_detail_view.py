from django.test import TestCase
from django.test.client import RequestFactory
from django.http import Http404

from tsuru_dashboard import settings
from tsuru_dashboard.apps.views import AppDetail

from mock import patch, Mock


class AppDetailTestCase(TestCase):
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
            "teams": ["tsuruteam", "crane"]
        }
        json_mock = Mock(status_code=200)
        json_mock.json.return_value = self.expected
        requests_mock.return_value = json_mock

        service_instances_mock = Mock()
        service_instances_mock.return_value = [{"service": "mongodb", "instances": ["mymongo"]}]

        self.old_service_instances = AppDetail.service_instances
        AppDetail.service_instances = service_instances_mock

        self.response = AppDetail.as_view()(request, app_name="app1")
        self.request = request

    def tearDown(self):
        AppDetail.service_instances = self.old_service_instances

    def test_should_use_detail_template(self):
        self.assertIn("apps/details.html", self.response.template_name)

    def test_should_get_the_app_info_from_tsuru(self):
        self.assertDictEqual(self.expected, self.response.context_data["app"])

    def test_service_instances_context(self):
        context = self.response.context_data
        service_instances = context["app"]["service_instances"]
        self.assertListEqual(service_instances, [{"name": "mymongo", "servicename": "mongodb"}])

    @patch('requests.get')
    def test_service_instances_empty(self, get):
        response = Mock(status_code=204)
        response.json.side_effect = ValueError
        get.return_value = response
        AppDetail.service_instances = self.old_service_instances
        app_detail = AppDetail()
        app_detail.request = self.request
        app_detail.service_instances("appname")
        get.assert_called_with(
            '{0}/services/instances?app=appname'.format(settings.TSURU_HOST),
            headers={'authorization': self.request.session.get('tsuru_token')})

    @patch("requests.get")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_not_found(self, token_is_valid, requests_mock):
        token_is_valid.return_value = True
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}
        requests_mock.return_value = Mock(status_code=404)

        service_instances_mock = Mock()
        service_instances_mock.return_value = [{"service": "mongodb", "instances": ["mymongo"]}]
        AppDetail.service_instances = service_instances_mock

        with self.assertRaises(Http404):
            AppDetail.as_view()(request, app_name="app1")
