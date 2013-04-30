from django.test import TestCase
from django.test.client import RequestFactory

from apps.views import AppDetail

from pluct.resource import Resource

import mock


class AppDetailTestCase(TestCase):
    @mock.patch("pluct.resource.get")
    def test_should_use_detail_template(self, get):
        request = RequestFactory().get("/")
        request.session = {"tsuru_token":"admin"}
        response = AppDetail.as_view()(request, app_name="app1")
        self.assertEqual("apps/details.html", response.template_name)

    @mock.patch("pluct.resource.get")
    def test_should_get_the_app_info_from_tsuru(self, get):
        request = RequestFactory().get("/")
        request.session = {"tsuru_token":"admin"}
        expected = {
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
            data=expected,
        )
        get.return_value = resource
        response = AppDetail.as_view()(request, app_name="app1")
        self.assertDictEqual(expected, response.context_data["app"])
