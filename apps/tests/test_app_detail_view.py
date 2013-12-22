from django.test import TestCase
from django.test.client import RequestFactory

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
        self.response = AppDetail.as_view()(request, app_name="app1")

    def test_should_use_detail_template(self):
        self.assertIn("apps/details.html", self.response.template_name)

    def test_should_get_the_app_info_from_tsuru(self):
        self.assertDictEqual(self.expected,
                             self.response.context_data["app"])
