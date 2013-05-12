from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory

from apps.views import ListApp


class ListAppViewTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}

    @patch('requests.get')
    def test_should_use_list_template(self, get):
        get.return_value = Mock(status_code=204)
        response = ListApp().get(self.request)
        self.assertEqual("apps/list.html", response.template_name)

    @patch('requests.get')
    def teste_should_get_list_of_apps_from_tsuru(self, get):
        expected = [{"framework": "python", "name": "pacote",
                     "repository": "git@tsuru.com:pacote.git",
                     "state": "creating"}]
        get.return_value = Mock(status_code=200, json=expected)
        response = ListApp().get(self.request)
        self.assertEqual([{"framework": "python", "name": "pacote",
                           "repository": "git@tsuru.com:pacote.git",
                           "state": "creating"}],
                         response.context_data.get("apps"))
