from mock import patch, Mock, call

from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.conf import settings

from auth.views import LoginRequiredView
from apps.views import AppLog


class AppLogViewTest(TestCase):
    @patch("requests.get")
    def setUp(self, get):
        self.request = RequestFactory().get("/")
        self.request.session = {'tsuru_token': 'tokentest'}
        self.app_name = 'app-teste'
        self.response = AppLog().get(self.request, self.app_name)

    def test_should_require_login_to_set_env(self):
        assert issubclass(AppLog, LoginRequiredView)

    def test_run_should_render_expected_template(self):
        self.assertEqual('apps/app_log.html', self.response.template_name)

    def test_context_should_contain_logs(self):
        self.assertIn('logs', self.response.context_data.keys())

    def test_context_should_contain_app(self):
        self.assertIn('app', self.response.context_data.keys())

    @patch('requests.get')
    def test_expected_calls(self, get):
        AppLog().get(self.request, self.app_name)
        authorization = {'authorization': self.request.session.get('tsuru_token')}

        calls = []

        url = "{}/apps/{}".format(settings.TSURU_HOST, self.app_name)
        calls.append(call(url, headers=authorization))

        url = "{}/apps/{}/log?lines=10".format(settings.TSURU_HOST, self.app_name)
        calls.append(call(url, headers=authorization))

        self.assertEqual(calls, get.call_args_list)

    @patch('requests.get')
    def test_should_return_expected_context(self, get):
        expected = [{"logs": "teste"}]
        response_mock = Mock()
        response_mock.json.return_value = expected
        get.return_value = response_mock
        response = AppLog().get(self.request, self.app_name)
        self.assertListEqual(expected, response.context_data['logs'])

    def test_get_request_run_url_should_not_return_404(self):
        response = self.client.get(reverse('app_log', args=[self.app_name]))
        self.assertNotEqual(404, response.status_code)
