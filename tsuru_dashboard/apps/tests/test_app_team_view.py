from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from tsuru_dashboard import settings
from tsuru_dashboard.apps.views import AppTeams


class AppTeamsViewTest(TestCase):

    @patch('requests.get')
    def setUp(self, get):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.session = {'tsuru_token': 'tokentest'}
        self.app_name = 'app-teste'
        self.response_mock = Mock()
        self.response_mock.status_code = 200
        self.response_mock.content = '{}'
        get.return_value = self.response_mock
        self.response = AppTeams.as_view()(self.request, app_name=self.app_name)

    def test_run_should_render_expected_template(self):
        self.assertIn('apps/app_team.html', self.response.template_name)

    def test_context_should_contain_app(self):
        self.assertIn('app', self.response.context_data.keys())

    @patch('requests.get')
    @patch('tsuru_dashboard.auth.views.token_is_valid')
    def test_get_sends_request_to_tsuru_with_args_expected(self, token_is_valid, get):
        AppTeams.as_view()(self.request, app_name=self.app_name)
        url = "{}/apps/{}".format(settings.TSURU_HOST, self.app_name)
        get.assert_called_with(
            url, headers={'authorization': self.request.session['tsuru_token']})

    @patch("requests.get")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_get_with_valid_app_should_return_expected_context(self, tis, get):
        tis.return_value = True
        expected = {
            "Name": "app1",
            "Framework": "php",
            "Repository": "git@git.com:php.git",
            "State": "dead",
            "Units": [
                {"Ip": "10.10.10.10"},
                {"Ip": "9.9.9.9"}
            ],
            "Teams": ["tsuruteam", "crane"]
        }
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = expected
        get.return_value = response_mock

        response = AppTeams.as_view()(self.request, app_name="app1")

        self.assertDictEqual(expected, response.context_data["app"])

    @patch('requests.get')
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_get_with_invalid_app_should_return_context_with_error(self, tis, get):
        self.response_mock.status_code = 404
        self.response_mock.content = 'App not found'
        get.return_value = self.response_mock

        response = AppTeams.as_view()(self.request, app_name='invalid-app')

        self.assertIn('errors', response.context_data.keys())
        self.assertEqual(self.response_mock.content, response.context_data['errors'])

    def test_get_request_run_url_should_not_return_404(self):
        response = self.client.get(reverse('app-teams', args=[self.app_name]))
        self.assertNotEqual(404, response.status_code)
