from mock import patch, Mock

from django.test import TestCase
from django.conf import settings
from django.test.client import RequestFactory

from apps.views import ListDeploy


class ListDeployViewTest(TestCase):
    @patch('requests.get')
    @patch("auth.views.token_is_valid")
    def setUp(self, token_is_valid, get):
        token_is_valid.return_value = True
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}
        self.response = ListDeploy.as_view()(self.request, app_name="appname")

    def test_context_should_contain_app(self):
        self.assertIn('app', self.response.context_data.keys())

    @patch('requests.get')
    @patch("auth.views.token_is_valid")
    def test_should_use_deploys_template(self, token_is_valid, get):
        token_is_valid.return_value = True
        get.return_value = Mock(status_code=200)
        self.assertEqual("apps/deploys.html", self.response.template_name)
        self.assertIn('deploys', self.response.context_data.keys())

    @patch('requests.get')
    @patch("auth.views.token_is_valid")
    def test_deploy_list(self, token_is_valid, get):
        token_is_valid.return_value = True
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}

        self.response = ListDeploy.as_view()(self.request, app_name="appname")

        url = '{}/deploys?app=appname&skip=0&limit=20'.format(settings.TSURU_HOST)
        headers = {'authorization': 'admin'}
        get.assert_called_with(url, headers=headers)

    @patch('requests.get')
    @patch("auth.views.token_is_valid")
    def test_empty_list(self, token_is_valid, get):
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = None
        get.return_value = response_mock
        token_is_valid.return_value = True

        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}

        ListDeploy.as_view()(request, app_name="appname")

        url = '{}/deploys?app=appname&skip=0&limit=20'.format(settings.TSURU_HOST)
        headers = {'authorization': 'admin'}
        get.assert_called_with(url, headers=headers)
