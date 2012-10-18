from django.test import TestCase
from django.test.client import RequestFactory

from apps.views import AppDetail

import mock


class AppDetailTestCase(TestCase):
    def test_should_use_detail_template(self):
        request = RequestFactory().get("/")
        request.session = {"tsuru_token":"admin"}
        with mock.patch("requests.get") as get:
            get.return_value = mock.Mock(status_code=200, json={})
            response = AppDetail.as_view()(request, app_name="app1")
        self.assertEqual("apps/detail.html", response.template_name)

    def test_should_get_the_app_info_from_tsuru(self):
        request = RequestFactory().get("/")
        request.session = {"tsuru_token":"admin"}
        expected = {
            "Name": "app1",
            "Framework": "php",
            "Repository": "git@git.com:php.git",
            "State": "dead",
            "Units": [
                {"Ip": "10.10.10.10"},
                {"Ip": "9.9.9.9"}
            ],
            "Teams": ["tsuruteam", "crane"]
        }
        with mock.patch("requests.get") as get:
            get.return_value = mock.Mock(status_code=200, json=expected)
            response = AppDetail.as_view()(request, app_name="app1")
        self.assertDictEqual(expected, response.context_data["app"])
