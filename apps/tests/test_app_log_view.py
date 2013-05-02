from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory
from django.http import Http404

from auth.views import LoginRequiredView
from apps.views import AppLog


class AppLogViewTest(TestCase):

    @patch("pluct.resource.get")
    def setUp(self, get):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.session = {'tsuru_token': 'tokentest'}
        self.app_name = 'app-teste'
        self.response_mock = Mock()
        self.response_mock.status_code = 200
        self.response_mock.content = '{}'
        self.response = AppLog().get(self.request, self.app_name)

    def test_should_require_login_to_set_env(self):
        assert issubclass(AppLog, LoginRequiredView)

    def test_run_should_render_expected_template(self):
        self.assertEqual('apps/app_log.html', self.response.template_name)

    def test_context_should_contain_logs(self):
        self.assertIn('logs', self.response.context_data.keys())

    def test_context_should_contain_app(self):
        self.assertIn('app', self.response.context_data.keys())

    def test_app_on_context_should_contain_app_name(self):
        self.assertEqual(self.app_name, self.response.context_data['app'])

    @patch('pluct.resource.get')
    def test_request_get_to_tsuru_with_args_expected(self, get):
        resource_mock = Mock()
        get.return_value = resource_mock
        AppLog().get(self.request, self.app_name)
        resource_mock.log.assert_called_with(lines=10)

    @patch('pluct.resource.get')
    def test_should_return_expected_context(self, get):
        expected = [{"logs": "teste"}]
        log_mock = Mock()
        log_mock.json.return_value = expected
        resource_mock = Mock()
        resource_mock.log.return_value = log_mock
        get.return_value = resource_mock
        response = AppLog().get(self.request, self.app_name)
        self.assertListEqual(expected, response.context_data['logs'])

    def test_get_request_run_url_should_return_200(self):
        try:
            self.client.get('/app/%s/log/' % self.app_name)
        except Http404:
            assert False
