# coding: utf-8
from mock import patch, Mock

from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory
from django.http import Http404

from auth.views import LoginRequiredView
from apps.views import AppEnv
from apps.forms import SetEnvForm


class AppEnvViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.session = {'tsuru_token': 'tokentest'}
        self.request_post = self.factory.post('/', {'env': 'env-test'})
        self.request_post.session = {}
        self.app_name = 'app-teste'
        self.response_mock = Mock()
        self.response_mock.status_code = 200
        self.response_mock.content = '{}'
        self.response_mock.content = 'env1\nenv2\n'
        self.view = AppEnv()
        self.view.get_envs = Mock(return_value=self.response_mock)
        with patch('requests.get') as get:
            get.return_value = self.response_mock
            self.response = AppEnv().get(self.request, self.app_name)

    def test_should_require_login_to_set_env(self):
        assert issubclass(AppEnv, LoginRequiredView)

    def test_run_should_render_expected_template(self):
        self.assertEqual('apps/app_env.html', self.response.template_name)

    def test_context_should_contain_envs(self):
        self.assertIn('envs', self.response.context_data.keys())

    def test_context_should_contain_app(self):
        self.assertIn('app', self.response.context_data.keys())

    def test_app_on_context_should_contain_app_name(self):
        self.assertEqual(self.app_name, self.response.context_data['app'])

    def test_get_with_app_should_send_request_get_to_tsuru_with_args_expected(self):
        with patch('requests.get') as get:
            AppEnv().get(self.request, self.app_name)
            get.assert_called_with('%s/apps/%s/env' % (settings.TSURU_HOST, self.app_name),
                                    headers={'authorization': self.request.session['tsuru_token']})

    def test_get_with_valid_app_should_return_expected_context(self):
        with patch('requests.get') as get:
            get.return_value = self.response_mock
            response = AppEnv().get(self.request, self.app_name)

            expected_response = self.response_mock.content.split('\n')
            self.assertEqual(expected_response, response.context_data['envs'])

    def test_get_with_invalid_app_should_return_context_with_error(self):
        self.response_mock.status_code = 404
        self.response_mock.content = 'App not found'

        with patch('requests.get') as get:
            get.return_value = self.response_mock
            response = AppEnv().get(self.request, 'invalid-app')

            self.assertIn('errors', response.context_data.keys())
            self.assertEqual(self.response_mock.content, response.context_data['errors'])

    def test_get_request_to_url_should_return_200(self):
        try:
            self.client.get('/app/%s/env/' % self.app_name)
        except Http404:
            assert False

    def test_context_should_contain_form(self):
        self.assertIn('form', self.response.context_data.keys())

    def test_form_in_context_should_has_a_instance_of_SetEnvForm(self):
        form = self.response.context_data.get('form')
        self.assertTrue(isinstance(form, SetEnvForm))

    def test_form_in_context_should_has_initial_app_name(self):
        form = self.response.context_data.get('form')
        self.assertTrue({'app': self.app_name}, form.initial)

    def test_post_with_app_and_env_should_send_request_post_to_tsuru_with_args_expected(self):
        self.request_post.session = {'tsuru_token': 'tokentest'}
        with patch('requests.post') as post:
            self.view.post(self.request_post, self.app_name)
            self.assertEqual(1, post.call_count)
            post.assert_called_with(u'%s/apps/%s/env' % (settings.TSURU_HOST, self.app_name),
                                    data=u'env-test',
                                    headers={'authorization': self.request_post.session['tsuru_token']})

    def test_post_with_valid_app_and_env_should_return_context_with_message_expected(self):
        with patch('requests.post') as post:
            self.response_mock.status_code = 200
            self.response_mock.content = "env added"
            post.side_effect = Mock(return_value=self.response_mock)
            response = self.view.post(self.request_post, self.app_name)
            self.assertEqual("env added", response.context_data.get('message'))

    def test_post_with_invalid_app_or_env_should_return_error_message_expected_on_context(self):
        with patch('requests.post') as post:
            self.response_mock.status_code = 500
            self.response_mock.content = 'Error'
            post.side_effect = Mock(return_value=self.response_mock)
            response = self.view.post(self.request_post, 'invalid-app')
            self.assertEqual('Error', response.context_data.get('errors'))

    def test_post_with_valid_app_and_env_should_return_context_with_form(self):
        with patch('requests.post') as post:
            self.response_mock.status_code = 200
            post.side_effect = Mock(return_value=self.response_mock)
            response = self.view.post(self.request_post, self.app_name)
            self.assertIn('form', response.context_data.keys())
            self.assertTrue(isinstance(response.context_data.get('form'), SetEnvForm))

    def test_post_without_env_should_return_form_with_errors(self):
        with patch('requests.post'):
            request = self.factory.post('/', {'env': ''})
            request.session = {}
            response = self.view.post(request, self.app_name)
            self.assertIn('form', response.context_data.keys())
            form = response.context_data.get('form')
            self.assertTrue(isinstance(form, SetEnvForm))
            self.assertEqual(u'This field is required.', form.errors.get('env')[0])

    def test_post_with_valid_app_should_return_env_list_of_envs_with_new_env(self):
        self.response_mock.content = 'env1\nenv2\n'
        with patch('requests.post') as post:
            post.return_value = self.response_mock
            response = self.view.post(self.request_post, self.app_name)

            expected_response = self.response_mock.content.split('\n')
            expected_response.append(self.request_post.POST['env'])
            self.assertIn('envs', response.context_data.keys())
            self.assertEqual(expected_response, response.context_data['envs'])

    def test_post_request_to_url_should_return_200(self):
        try:
            self.client.post('/app/%s/env/' % self.app_name, self.request_post.POST)
        except Http404:
            assert False
