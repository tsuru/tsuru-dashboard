from mock import patch
from django.test import TestCase
from django.test.client import RequestFactory
from tsuru_dashboard.components.views import ListComponentJson
import json


class ListComponentJsonViewTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "token", "permissions": {"admin": True}}

    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_list_components(self, token_is_valid):
        token_is_valid.return_value = True
        expected = {
            "components": [
                "registry",
                "big-sibling"
            ]
        }
        response = ListComponentJson.as_view()(self.request)
        self.assertDictEqual(expected, json.loads(response.content))
