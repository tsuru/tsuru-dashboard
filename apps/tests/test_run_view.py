from mock import patch, Mock

from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory
from django.http import Http404

from auth.views import LoginRequiredView
from apps.views import Run
from apps.forms import RunForm


class RunViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.response = Run().get(self.request)
        self.request_post = self.factory.post('/', {'app': 'app-test', 'command': 'command-test'})
        self.request_post.session = {}
        self.response_mock = Mock()

    def test_should_require_login_to_create_team(self):
        assert issubclass(Run, LoginRequiredView)

    def test_run_should_render_expected_template(self):
        self.assertEqual('apps/run.html', self.response.template_name)

    def test_context_should_contain_form(self):
        self.assertIn('form', self.response.context_data.keys())

    def test_form_in_context_should_has_a_instance_of_RunForm(self):
        form = self.response.context_data.get('form')
        self.assertTrue(isinstance(form, RunForm))

    def test_get_request_run_url_should_return_200(self):
        try:
            self.client.get('/app/run/')
        except Http404:
            assert False

    def test_post_with_app_and_command_should_send_request_post_to_tsuru_with_args_expected(self):
        self.request_post.session = {'tsuru_token': 'tokentest'}
        with patch('requests.post') as post:
            Run().post(self.request_post)
            self.assertEqual(1, post.call_count)
            post.assert_called_with('%s/apps/app-test/run' % settings.TSURU_HOST,
                                    data=u'command-test',
                                    headers={'authorization': self.request_post.session['tsuru_token']})

    def test_post_with_valid_app_and_command_should_return_context_with_message_expected(self):
        with patch('requests.post') as post:
            self.response_mock.status_code = 200
            post.side_effect = Mock(return_value=self.response_mock)
            response = Run().post(self.request_post)
            self.assertEqual("The Command was executed with successfully", response.context_data.get('message'))

    def test_post_with_invalid_app_or_command_should_return_error_message_expected_on_context(self):
        with patch('requests.post') as post:
            self.response_mock.status_code = 500
            self.response_mock.content = 'Error'
            post.side_effect = Mock(return_value=self.response_mock)
            response = Run().post(self.request_post)
            self.assertEqual('Error', response.context_data.get('errors'))

    def test_post_with_valid_app_and_command_should_return_context_with_form(self):
        with patch('requests.post') as post:
            self.response_mock.status_code = 200
            post.side_effect = Mock(return_value=self.response_mock)
            response = Run().post(self.request_post)
            self.assertIn('form', response.context_data.keys())
            self.assertTrue(isinstance(response.context_data.get('form'), RunForm))

    def test_post_with_invalid_app_or_command_should_return_context_with_form(self):
        with patch('requests.post') as post:
            self.response_mock.status_code = 500
            self.response_mock.content = 'Error'
            post.side_effect = Mock(return_value=self.response_mock)
            response = Run().post(self.request_post)
            self.assertIn('form', response.context_data.keys())
            self.assertTrue(isinstance(response.context_data.get('form'), RunForm))

    def test_post_without_app_should_not_send_request_to_tsuru(self):
        with patch('requests.post') as post:
            request = self.factory.post('/', {'app': '', 'command': 'comand-test'})
            request.session = {}
            Run().post(request)
            self.assertEqual(0, post.call_count)

    def test_post_without_app_should_return_form_with_errors(self):
        with patch('requests.post'):
            request = self.factory.post('/', {'app': '', 'command': 'command-test'})
            request.session = {}
            response = Run().post(request)
            self.assertIn('form', response.context_data.keys())
            form = response.context_data.get('form')
            self.assertTrue(isinstance(form, RunForm))
            self.assertEqual(u'This field is required.', form.errors.get('app')[0])
