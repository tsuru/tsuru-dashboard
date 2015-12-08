from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory

from tsuru_dashboard import settings
from tsuru_dashboard.apps.views import ListAppJson

import json


class ListAppJsonViewTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}

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

        response = ListAppJson.as_view()(self.request)

        expected = {
            "apps": [{
                "framework": "python",
                "name": "pacote",
                "repository": "git@tsuru.com:pacote.git",
                "state": "creating",
            }]
        }
        self.assertDictEqual(expected, json.loads(response.content))
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
        response = ListAppJson.as_view()(request)

        expected = {
            "apps": [{
                "framework": "python",
                "name": "pacote",
                "repository": "git@tsuru.com:pacote.git",
                "state": "creating",
            }]
        }
        self.assertDictEqual(expected, json.loads(response.content))
        url = "{}/apps?name=pacote".format(settings.TSURU_HOST)
        get.assert_called_with(url, headers={'authorization': 'admin'})
