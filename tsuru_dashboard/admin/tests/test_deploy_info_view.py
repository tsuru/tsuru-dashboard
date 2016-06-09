import copy

from django.test import TestCase
from django.test.client import RequestFactory
from django.http import Http404

from tsuru_dashboard import settings
from tsuru_dashboard.admin.views import DeployInfo

from mock import patch, Mock


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

    @patch("requests.get")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_view(self, token_is_valid, get):
        token_is_valid.return_value = True
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = copy.deepcopy(self.data)
        get.return_value = response_mock
        response = DeployInfo.as_view()(self.request,
                                        deploy="53e143cb874ccb1f68000001")
        self.assertIn("deploys/deploy_details.html", response.template_name)
        expected = copy.deepcopy(self.data)
        diff = u"<div class=\"highlight\"><pre><span></span>%s\n</pre></div>\n"
        expected["Diff"] = diff % self.data["Diff"]
        self.assertDictEqual(expected, response.context_data['deploy'])
        get.assert_called_with(
            '{0}/deploys/{1}'.format(settings.TSURU_HOST,
                                     "53e143cb874ccb1f68000001"),
            headers={'authorization': 'admin'}
        )

    @patch("requests.get")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_view_without_diff(self, token_is_valid, get):
        token_is_valid.return_value = True
        data = copy.deepcopy(self.data)
        del data["Diff"]
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = copy.deepcopy(data)
        get.return_value = response_mock
        response = DeployInfo.as_view()(self.request, deploy="53e143cb874ccb1f68000001")
        self.assertIn("deploys/deploy_details.html", response.template_name)
        expected = copy.deepcopy(data)
        expected["Diff"] = None
        self.assertDictEqual(expected, response.context_data["deploy"])
        get.assert_called_with(
            '{0}/deploys/{1}'.format(settings.TSURU_HOST, "53e143cb874ccb1f68000001"),
            headers={'authorization': 'admin'}
        )

    @patch("requests.get")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_view_on_error(self, token_is_valid, get):
        token_is_valid.return_value = True
        response_mock = Mock(status_code=404)
        error_msg = "No JSON object could be decoded"
        response_mock.json.side_effect = ValueError(error_msg)
        get.return_value = response_mock

        with self.assertRaises(Http404):
            DeployInfo.as_view()(self.request, deploy="53e143cb874ccb1f68000001")
