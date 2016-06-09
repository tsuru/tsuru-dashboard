import copy
import json

from django.test import TestCase
from django.test.client import RequestFactory

from tsuru_dashboard import settings
from tsuru_dashboard.apps.views import DeployInfo

from mock import patch, Mock

import httpretty


class InfoViewTest(TestCase):

    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}
        self.data = {u'Id': u'53e143cb874ccb1f68000001',
                     u'App': u'g1',
                     u'Timestamp': u'18-08-2014 11:29:32',
                     u'Duration': u'00m23s',
                     u'Commit': u'e82nn93nd93mm12o2ueh83dhbd3iu112',
                     u'Error': u'',
                     u'Diff': u'test_diff'}

    @httpretty.activate
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_view(self, token_is_valid):
        token_is_valid.return_value = True

        url = '{}/deploys/{}'.format(settings.TSURU_HOST, "53e143cb874ccb1f68000001")
        body = json.dumps(self.data)
        httpretty.register_uri(httpretty.GET, url, body=body)

        url = '{}/apps/{}'.format(settings.TSURU_HOST, "app_name")
        body = json.dumps({"name": "app_name"})
        httpretty.register_uri(httpretty.GET, url, body=body)

        view = DeployInfo
        response = view.as_view()(
            self.request,
            deploy="53e143cb874ccb1f68000001",
            app_name="app_name",
        )

        expected = copy.deepcopy(self.data)
        diff = u"""<div class="highlight"><pre><span></span>%s\n</pre></div>\n"""
        expected["Diff"] = diff % self.data["Diff"]
        self.assertEqual("apps/deploy.html", response.template_name[0])
        self.assertDictEqual(expected, response.context_data['deploy'])
        self.assertIn('app', response.context_data.keys())

    @patch("requests.get")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_view_without_diff(self, token_is_valid, get):
        token_is_valid.return_value = True
        data = copy.deepcopy(self.data)
        del data["Diff"]
        response_mock = Mock()
        response_mock.json.return_value = copy.deepcopy(data)
        get.return_value = response_mock

        view = DeployInfo
        view.get_app = Mock()
        response = view.as_view()(
            self.request,
            deploy="53e143cb874ccb1f68000001",
            app_name="app_name",
        )

        data["Diff"] = None

        self.assertEqual("apps/deploy.html", response.template_name[0])
        self.assertDictEqual(data, response.context_data['deploy'])
        self.assertIn('app', response.context_data.keys())
        url = '{0}/deploys/{1}'.format(settings.TSURU_HOST, "53e143cb874ccb1f68000001")
        get.assert_called_with(url, headers={'authorization': 'admin'})
