from mock import patch

from django.test import TestCase
from django.test.client import RequestFactory

from tsuru_dashboard.apps.views import ListApp


class ListAppViewTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}

    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_should_use_list_template(self, token_is_valid):
        token_is_valid.return_value = True
        response = ListApp.as_view()(self.request)
        self.assertIn("apps/list.html", response.template_name)
