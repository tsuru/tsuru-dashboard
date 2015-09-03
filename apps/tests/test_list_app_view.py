from mock import patch, Mock

from django.conf import settings
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
    def teste_list_apps(self, get):
        expected = [{
            "framework": "python",
            "name": "pacote",
            "repository": "git@tsuru.com:pacote.git",
            "state": "creating"
        }]
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = expected
        get.return_value = response_mock

        response = ListApp.as_view()(self.request)

        expected = [{
            "framework": "python",
            "name": "pacote",
            "repository": "git@tsuru.com:pacote.git",
            "state": "creating",
        }]
        self.assertListEqual(expected, response.context_data["apps"])
        url = "{}/apps".format(settings.TSURU_HOST)
        get.assert_called_with(url, headers={'authorization': 'admin'})

    @patch('requests.get')
    def teste_list_apps_by_name(self, get):
        expected = [{
            "framework": "python",
            "name": "pacote",
            "repository": "git@tsuru.com:pacote.git",
            "state": "creating"
        }]
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = expected
        get.return_value = response_mock

        request = RequestFactory().get("/?name=pacote")
        request.session = {"tsuru_token": "admin"}
        response = ListApp.as_view()(request)

        expected = [{
            "framework": "python",
            "name": "pacote",
            "repository": "git@tsuru.com:pacote.git",
            "state": "creating",
        }]
        self.assertListEqual(expected, response.context_data["apps"])
        url = "{}/apps?name=pacote".format(settings.TSURU_HOST)
        get.assert_called_with(url, headers={'authorization': 'admin'})
