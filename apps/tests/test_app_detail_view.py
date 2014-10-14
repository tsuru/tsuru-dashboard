import json

from django.test import TestCase
from django.test.client import RequestFactory
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
                {"Ip": "10.10.10.10"},
                {"Ip": "9.9.9.9"}
            ],
            "teams": ["tsuruteam", "crane"]
        }
        json_mock = Mock()
        json_mock.json.return_value = self.expected
        requests_mock.return_value = json_mock

        service_list_mock = Mock()
        service_list_mock.return_value = [{"service": "mongodb",
                                           "instances": ["mymongo"]}]
        service_info_mock = Mock()
        service_info_mock.return_value = {"Name": "mymongo",
                                          "ServiceName": "mongodb",
                                          "Apps": ["app1"]}

        self.old_service_list = AppDetail.service_list
        AppDetail.service_list = service_list_mock
        self.old_service_info = AppDetail.service_info
        AppDetail.service_info = service_info_mock

        self.response = AppDetail.as_view()(request, app_name="app1")
        self.request = request

    def tearDown(self):
        AppDetail.service_info = self.old_service_info
        AppDetail.service_list = self.old_service_list

    def test_should_use_detail_template(self):
        self.assertIn("apps/details.html", self.response.template_name)

    @patch('requests.get')
    def test_get_envs(self, get):
        expected = [{"name": "DATABASE_HOST", "value": "localhost", "public": True}]
        response_mock = Mock()
        response_mock.json.return_value = expected
        get.return_value = response_mock

        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}

        app_detail = AppDetail()
        app_detail.request = request
        envs = app_detail.get_envs("appname")

        self.assertListEqual(envs, expected)
        url = '{}/apps/appname/env'.format(settings.TSURU_HOST)
        get.assert_called_with(url, headers={'authorization': 'admin'})

    @patch('requests.get')
    def test_get_containers(self, get):
        expected = []
        response_mock = Mock()
        response_mock.json.return_value = expected
        get.return_value = response_mock

        request = RequestFactory().get("/")
        request.session = {"is_admin": True, "tsuru_token": "admin"}

        app_detail = AppDetail()
        app_detail.request = request
        envs = app_detail.get_containers("appname")

        self.assertListEqual(envs, expected)
        url = '{}/docker/node/apps/appname/containers'.format(settings.TSURU_HOST)
        get.assert_called_with(url, headers={'authorization': 'admin'})

    def test_should_get_the_app_info_from_tsuru(self):
        self.assertDictEqual(self.expected,
                             self.response.context_data["app"])

    def test_service_instances(self):
        context = self.response.context_data
        service_instances = context["app"]["service_instances"]
        self.assertListEqual(service_instances, [{"name": "mymongo",
                                                  "servicename": "mongodb"}])

    @patch('requests.get')
    def test_service_list(self, get):
        AppDetail.service_list = self.old_service_list
        app_detail = AppDetail()
        app_detail.request = self.request
        app_detail.service_list()
        get.assert_called_with(
            '{0}/services/instances'.format(settings.TSURU_HOST),
            headers={'authorization': self.request.session.get('tsuru_token')})

    @patch('requests.get')
    def test_service_info_with_invalid_instance_name(self, get):
        AppDetail.service_info = self.old_service_info
        app_detail = AppDetail()
        app_detail.request = self.request
        instance_name = "shubiduba"
        app_detail.service_info(instance_name)
        get.assert_called_with(
            '{0}/services/instances/{1}'.format(settings.TSURU_HOST,
                                                instance_name),
            headers={'authorization': self.request.session.get('tsuru_token')})

    @patch('requests.get')
    def test_service_info(self, get):
        instance_name = u"""{"Name": "mymongo", "ServiceName": "mongodb",
                        "Apps": ["app1"]}"""
        m = Mock(status_code=200, content=instance_name)
        m.json.return_value = json.loads(instance_name)
        get.return_value = m
        request = RequestFactory().get("/")
        request.session = {}
        AppDetail.service_info = self.old_service_info
        app_detail = AppDetail()
        app_detail.request = self.request
        app_detail.service_info(instance_name)
        get.assert_called_with(
            '{0}/services/instances/{1}'.format(settings.TSURU_HOST,
                                                instance_name),
            headers={'authorization': self.request.session.get('tsuru_token')})
