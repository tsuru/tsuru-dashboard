from django.test import TestCase
from django.test.client import RequestFactory
from django.conf import settings

from apps.views import AppDetail

from pluct.resource import Resource
from pluct.schema import Schema

import mock


class AppDetailTestCase(TestCase):
    @mock.patch("requests.get")
    @mock.patch("pluct.resource.get")
    def setUp(self, get, requests_mock):
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
        schema = Schema(
            "",
            type="object",
            properties={
                "units":
                {
                    "type": "array",
                    "items": {},
                },
                "teams":
                {
                    "type": "array",
                    "items": {},
                }
            }
        )
        resource = Resource(
            url="url.com",
            data=self.expected,
            schema=schema
        )
        get.return_value = resource
        json_mock = mock.Mock()
        json_mock.json.return_value = self.expected
        requests_mock.return_value = json_mock
        service_list_mock = mock.Mock()
        service_list_mock.return_value = [{"service": "mongodb", "instances": ["mymongo"]}]
        service_info_mock = mock.Mock()
        service_info_mock.return_value = {"Name": "mymongo", "ServiceName": "mongodb", "Apps": ["app1"]}
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

    def test_should_get_the_app_info_from_tsuru(self):
        self.assertDictEqual(self.expected,
                             self.response.context_data["app"])

    def test_service_instances(self):
        service_instances = self.response.context_data["app"]["service_instances"]
        self.assertListEqual(service_instances, [{"name": "mymongo", "servicename": "mongodb"}])

    @mock.patch('requests.get')
    def test_service_list(self, get):
        AppDetail.service_list = self.old_service_list
        app_detail = AppDetail()
        app_detail.request = self.request
        app_detail.service_list()
        get.assert_called_with(
            '{0}/services'.format(settings.TSURU_HOST),
            headers={'authorization': self.request.session.get('tsuru_token')})

    @mock.patch('requests.get')
    def test_service_info(self, get):
        AppDetail.service_info = self.old_service_info
        app_detail = AppDetail()
        app_detail.request = self.request
        instance_name = "shubiduba"
        app_detail.service_info(instance_name)
        get.assert_called_with(
            '{0}/services/instances/{1}'.format(settings.TSURU_HOST, instance_name),
            headers={'authorization': self.request.session.get('tsuru_token')})
