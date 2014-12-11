from mock import patch

from django.test import TestCase
from django.conf import settings
from django.test.client import RequestFactory

from apps.views import ListDeploy


class ListDeployViewTest(TestCase):
    @patch('requests.get')
    def setUp(self, get):
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}
        self.response = ListDeploy.as_view()(self.request, app_name="appname")

    def test_context_should_contain_app(self):
        self.assertIn('app', self.response.context_data.keys())

    @patch('requests.get')
    def test_should_use_deploys_template(self, get):
        self.assertEqual("apps/deploys.html", self.response.template_name)
        self.assertIn('deploys', self.response.context_data.keys())

    @patch('requests.get')
    def test_deploy_list(self, get):
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}

        self.response = ListDeploy.as_view()(self.request, app_name="appname")

        url = '{}/deploys?app=appname'.format(settings.TSURU_HOST)
        headers = {'authorization': 'admin'}
        get.assert_called_with(url, headers=headers)
