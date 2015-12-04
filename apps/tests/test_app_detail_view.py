from django.test import TestCase
from django.test.client import RequestFactory
from django.http import Http404
from django.conf import settings

from apps.views import AppDetail

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
        self.old_get_containers = AppDetail.get_containers
        AppDetail.service_instances = service_instances_mock
        AppDetail.get_containers = lambda x, y: []

        self.response = AppDetail.as_view()(request, app_name="app1")
        self.request = request

    def tearDown(self):
        AppDetail.service_instances = self.old_service_instances
        AppDetail.get_containers = self.old_get_containers

    def test_should_use_detail_template(self):
        self.assertIn("apps/details.html", self.response.template_name)

    def test_units_by_status(self):
        self.assertIn("units_by_status", self.response.context_data)

        expected = {
            'started': [{'Ip': '10.10.10.10', 'Status': 'started', 'ProcessName': 'web'}],
            'stopped': [{'Ip': '9.9.9.9', 'Status': 'stopped', 'ProcessName': 'worker'}],
        }
        self.assertDictEqual(expected, self.response.context_data['units_by_status'])

    @patch('requests.get')
    def test_get_containers(self, get):
        expected = []
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = expected
        get.return_value = response_mock

        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}

        AppDetail.get_containers = self.old_get_containers
        app_detail = AppDetail()
        app_detail.request = request
        envs = app_detail.get_containers("appname")

        self.assertListEqual(envs, expected)
        url = '{}/docker/node/apps/appname/containers'.format(settings.TSURU_HOST)
        get.assert_called_with(url, headers={'authorization': 'admin'})

    @patch('requests.get')
    def test_get_containers_forbidden(self, get):
        response_mock = Mock(status_code=403)
        get.return_value = response_mock

        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}

        AppDetail.get_containers = self.old_get_containers
        app_detail = AppDetail()
        app_detail.request = request
        envs = app_detail.get_containers("appname")

        self.assertEqual([], envs)
        url = '{}/docker/node/apps/appname/containers'.format(settings.TSURU_HOST)
        get.assert_called_with(url, headers={'authorization': 'admin'})

    def test_should_get_the_app_info_from_tsuru(self):
        self.assertDictEqual(self.expected, self.response.context_data["app"])

    def test_service_instances_context(self):
        context = self.response.context_data
        service_instances = context["app"]["service_instances"]
        self.assertListEqual(service_instances, [{"name": "mymongo", "servicename": "mongodb"}])

    @patch('requests.get')
    def test_service_instances(self, get):
        get.return_value = Mock(status_code=200)
        AppDetail.service_instances = self.old_service_instances
        app_detail = AppDetail()
        app_detail.request = self.request
        app_detail.service_instances("appname")
        get.assert_called_with(
            '{0}/services/instances?app=appname'.format(settings.TSURU_HOST),
            headers={'authorization': self.request.session.get('tsuru_token')})

    @patch("requests.get")
    @patch("auth.views.token_is_valid")
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

    def test_process_list(self):
        app = {
            "units": [
                {"ProcessName": "web"},
                {"ProcessName": "web"},
                {"ProcessName": "web"},
                {"ProcessName": "worker"},
            ],
        }
        process_list = AppDetail().process_list(app)

        expected = set(["web", "worker"])
        self.assertEqual(expected, process_list)

    def test_process_list_without_units(self):
        app = {}
        process_list = AppDetail().process_list(app)

        expected = set()
        self.assertEqual(expected, process_list)

    def test_process_list_units_without_process_name(self):
        app = {
            "units": [
                {"ip": "0.0.0.0"},
                {"ip": "0.0.0.1"},
                {"ip": "0.0.0.2"},
                {"ip": "0.0.0.3"},
            ],
        }
        process_list = AppDetail().process_list(app)

        expected = set()
        self.assertEqual(expected, process_list)

    def test_process_list_in_context(self):
        self.assertIn('process_list', self.response.context_data)

        expected = set(["web", "worker"])
        self.assertEqual(expected, self.response.context_data['process_list'])
