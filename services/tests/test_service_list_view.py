from mock import patch

from django.test import TestCase
from django.test.client import RequestFactory

from services.views import ListService


class ListServiceViewTest(TestCase):
    @patch('pluct.resource.get')
    def test_should_use_list_template(self, get):
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}
        response = ListService.as_view()(request)
        self.assertEqual("services/list.html", response.template_name)
