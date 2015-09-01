from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory

from apps.views import ListApp


class ListAppViewTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}

    @patch('requests.get')
    @patch("auth.views.token_is_valid")
    def test_should_use_list_template(self, token_is_valid, get):
        token_is_valid.return_value = True
        get.return_value = Mock(status_code=204)
        response = ListApp.as_view()(self.request)
        self.assertIn("apps/list.html", response.template_name)
        self.assertListEqual([], response.context_data['apps'])

    @patch('requests.get')
    def teste_should_get_list_of_apps_from_tsuru(self, get):
        expected = [{"framework": "python", "name": "pacote",
                     "repository": "git@tsuru.com:pacote.git",
                     "state": "creating"}]
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = expected
        get.return_value = response_mock
        response = ListApp.as_view()(self.request)
        self.assertListEqual([{"framework": "python", "name": "pacote",
                               "repository": "git@tsuru.com:pacote.git",
                               "state": "creating"}],
                             response.context_data["apps"])
