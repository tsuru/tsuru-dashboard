import json

from mock import patch, Mock

from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory

from admin.views import ListDeploy


class ListDeployViewTest(TestCase):
    @patch('requests.get')
    def setUp(self, get):
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}
        content = u"""[{"Name":"mymongo"},{"Name":"yourssql"}]"""
        m = Mock(status_code=200, content=content)
        m.json.return_value = json.loads(content)
        get.return_value = m
        self.response = ListDeploy().get(self.request)
        self.response_mock = Mock()

    def test_context_should_contain_services(self):
        self.assertIn('services', self.response.context_data.keys())

    @patch('requests.get')
    def test_should_use_list_template(self, get):
        response_mock = Mock()
        response_mock.json.return_value = []
        get.return_value = response_mock
        request = RequestFactory().get("/?page=1")
        request.session = {"tsuru_token": "admin"}
        response = ListDeploy.as_view()(request)
        self.assertEqual("deploys/list_deploys.html", response.template_name)
        self.assertIn('deploys', response.context_data.keys())
        get.assert_called_with(
            '{0}/deploys?service=&skip=0&limit=20'.format(settings.TSURU_HOST),
            headers={'authorization': 'admin'})

    @patch('requests.get')
    def test_should_return_empty_list_when_status_is_204(self, get):
        content = u"""[{"Name":"mymongo"},{"Name":"yourssql"}]"""
        m = Mock(status_code=204, content=content)
        m.json.return_value = json.loads(content)
        get.return_value = m
        response = ListDeploy.as_view()(self.request)
        self.assertEqual("deploys/list_deploys.html", response.template_name)
        self.assertListEqual([], response.context_data['deploys'])
        get.assert_called_with(
            '{0}/deploys?service=&skip=0&limit=20'.format(settings.TSURU_HOST),
            headers={'authorization': 'admin'})
