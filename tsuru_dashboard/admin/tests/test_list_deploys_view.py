import json
import httpretty
import mock

from django.test import TestCase
from django.test.client import RequestFactory

from tsuru_dashboard import settings
from tsuru_dashboard.admin.views import ListDeploy


class ListDeployViewTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/?page=2")
        self.request.session = {"tsuru_token": "admin"}

    @httpretty.activate
    @mock.patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_should_use_list_template(self, token_is_valid):
        token_is_valid.return_value = True

        url = '{}/deploys?skip=0&limit=20'.format(settings.TSURU_HOST)
        body = json.dumps(range(10000))
        httpretty.register_uri(httpretty.GET, url, body=body, status=200)

        response = ListDeploy.as_view()(self.request)

        self.assertIn("deploys/list_deploys.html", response.template_name)
        self.assertIn('deploys', response.context_data.keys())
        self.assertEqual(3, response.context_data["next"])
        self.assertEqual(1, response.context_data["previous"])

    @httpretty.activate
    @mock.patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_should_return_empty_list_when_status_is_204(self, token_is_valid):
        token_is_valid.return_value = True

        url = '{}/deploys?skip=0&limit=20'.format(settings.TSURU_HOST)
        httpretty.register_uri(httpretty.GET, url, status=204)

        response = ListDeploy.as_view()(self.request)

        self.assertIn("deploys/list_deploys.html", response.template_name)
        self.assertListEqual([], response.context_data['deploys'])
