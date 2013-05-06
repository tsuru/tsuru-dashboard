# coding: utf-8
from mock import patch, Mock

from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from auth.views import LoginRequiredView
from apps.views import AppEnv
from apps.forms import SetEnvForm


class AppEnvViewTest(TestCase):

    @patch('requests.get')
    def setUp(self, get):
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

    @patch('requests.get')
    def test_get_with_app_should_send_request_to_tsuru(self, get):
        AppEnv().get(self.request, self.app_name)
        get.assert_called_with(
            '%s/apps/%s/env' % (settings.TSURU_HOST, self.app_name),
            headers={'authorization': self.request.session['tsuru_token']})

    @patch('requests.get')
    def test_get_with_valid_app_should_return_expected_context(self, get):
        get.return_value = self.response_mock
        response = AppEnv().get(self.request, self.app_name)

        expected_response = self.response_mock.content.split('\n')
        self.assertEqual(expected_response, response.context_data['envs'])

    @patch('requests.get')
    def test_get_with_invalid_app_should_return_context_with_error(self, get):
        self.response_mock.status_code = 404
        self.response_mock.content = 'App not found'

        get.return_value = self.response_mock
        response = AppEnv().get(self.request, 'invalid-app')

        self.assertIn('errors', response.context_data.keys())
        self.assertEqual(self.response_mock.content,
                         response.context_data['errors'])

    def test_get_request_to_url_should_not_return_404(self):
        response = self.client.get(reverse('get-env', args=[self.app_name]))
        self.assertNotEqual(404, response.status_code)

    def test_context_should_contain_form(self):
        self.assertIn('form', self.response.context_data.keys())

    def test_form_in_context_should_has_a_instance_of_SetEnvForm(self):
        form = self.response.context_data.get('form')
        self.assertTrue(isinstance(form, SetEnvForm))

    def test_form_in_context_should_has_initial_app_name(self):
        form = self.response.context_data.get('form')
        self.assertTrue({'app': self.app_name}, form.initial)

    @patch('requests.post')
    def test_post_should_send_request_post_to_tsuru(self, post):
        self.request_post.session = {'tsuru_token': 'tokentest'}
        self.view.post(self.request_post, self.app_name)
        self.assertEqual(1, post.call_count)
        post.assert_called_with(
            u'%s/apps/%s/env' % (settings.TSURU_HOST, self.app_name),
            data=u'env-test',
            headers={'authorization':
                     self.request_post.session['tsuru_token']})

    @patch('requests.post')
    def test_postshould_return_context_with_message_expected(self, post):
        self.response_mock.status_code = 200
        self.response_mock.content = "env added"
        post.side_effect = Mock(return_value=self.response_mock)
        response = self.view.post(self.request_post, self.app_name)
        self.assertEqual("env added", response.context_data.get('message'))

    @patch('requests.post')
    def test_invalid_post_should_return_error_message(self, post):
        self.response_mock.status_code = 500
        self.response_mock.content = 'Error'
        post.side_effect = Mock(return_value=self.response_mock)
        response = self.view.post(self.request_post, 'invalid-app')
        self.assertEqual('Error', response.context_data.get('errors'))

    @patch('requests.post')
    def test_valid_post_returns_context_with_form(self, post):
        self.response_mock.status_code = 200
        post.side_effect = Mock(return_value=self.response_mock)
        response = self.view.post(self.request_post, self.app_name)
        self.assertIn('form', response.context_data.keys())
        self.assertTrue(isinstance(response.context_data.get('form'),
                                   SetEnvForm))

    @patch('requests.post')
    def test_post_without_env_should_return_form_with_errors(self, post):
        request = self.factory.post('/', {'env': ''})
        request.session = {}
        response = self.view.post(request, self.app_name)
        self.assertIn('form', response.context_data.keys())
        form = response.context_data.get('form')
        self.assertTrue(isinstance(form, SetEnvForm))
        self.assertEqual(u'This field is required.',
                         form.errors.get('env')[0])

    @patch('requests.post')
    def test_post_with_valid_app_returns_env_list(self, post):
        self.response_mock.content = 'env1\nenv2\n'
        post.return_value = self.response_mock
        response = self.view.post(self.request_post, self.app_name)
        expected_response = self.response_mock.content.split('\n')
        expected_response.append(self.request_post.POST['env'])
        self.assertIn('envs', response.context_data.keys())
        self.assertEqual(expected_response, response.context_data['envs'])

    def test_post_request_to_url_should_not_return_404(self):
        response = self.client.post(reverse('get-env', args=[self.app_name]),
                                    self.request_post.POST)
        self.assertNotEqual(404, response.status_code)
