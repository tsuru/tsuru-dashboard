import json

from datetime import datetime
from mock import patch, Mock

from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory
from django.http import Http404

from auth.views import LoginRequiredView
from apps.views import AppLog


class AppLogViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.session = {'tsuru_token': 'tokentest'}
        self.app_name = 'app-teste'
        self.response_mock = Mock()
        self.response_mock.status_code = 200
        self.response_mock.content = '{}'
        with patch('requests.get') as get:
            get.return_value = self.response_mock
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

    def test_get_with_app_should_send_request_get_to_tsuru_with_args_expected(self):
        with patch('requests.get') as get:
            AppLog().get(self.request, self.app_name)
            get.assert_called_with('%s/apps/%s/log' % (settings.TSURU_HOST, self.app_name),
                                    headers={'authorization': self.request.session['tsuru_token']})

    def test_get_with_valid_app_should_return_expected_context(self):
        self.response_mock.content = '[{"logs": "teste"}]'
        with patch('requests.get') as get:
            get.return_value = self.response_mock
            response = AppLog().get(self.request, self.app_name)

            self.assertEqual(json.loads(self.response_mock.content), response.context_data['logs'])

    def test_get_with_invalid_app_should_return_context_with_error(self):
        self.response_mock.status_code = 404
        self.response_mock.content = 'App not found'

        with patch('requests.get') as get:
            get.return_value = self.response_mock
            response = AppLog().get(self.request, 'invalid-app')

            self.assertIn('errors', response.context_data.keys())
            self.assertEqual(self.response_mock.content, response.context_data['errors'])

    def test_get_request_run_url_should_return_200(self):
        try:
            self.client.get('/app/%s/log/' % self.app_name)
        except Http404:
            assert False
