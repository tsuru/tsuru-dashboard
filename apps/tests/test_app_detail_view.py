from django.test import TestCase
from django.test.client import RequestFactory

from apps.views import AppDetail

from pluct.resource import Resource

import mock


class AppDetailTestCase(TestCase):
    @mock.patch("pluct.resource.get")
    def setUp(self, get):
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
        resource = Resource(
            url="url.com",
            data=self.expected,
        )
        get.return_value = resource
        self.response = AppDetail.as_view()(request, app_name="app1")

    def test_should_use_detail_template(self):
        self.assertIn("apps/details.html", self.response.template_name)

    def test_should_get_the_app_info_from_tsuru(self):
        self.assertDictEqual(self.expected,
                             self.response.context_data["app"].data)
