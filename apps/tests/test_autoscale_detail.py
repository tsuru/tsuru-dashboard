from django.test import TestCase
from django.test.client import RequestFactory

from apps.views import AutoscaleDetail

from mock import patch


class AutoscaleDetailTest(TestCase):
    @patch("requests.get")
    def setUp(self, requests_mock):
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}

        self.response = AutoscaleDetail.as_view()(request, app_name="app1")
        self.request = request

    def test_should_use_detail_template(self):
        self.assertIn("apps/autoscale.html", self.response.template_name)

    def test_should_get_the_app_info_from_tsuru(self):
        self.assertIn("app", self.response.context_data)
