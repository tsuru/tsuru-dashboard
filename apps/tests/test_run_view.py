from mock import patch, Mock

from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory

from auth.views import LoginRequiredView
from apps.views import Run
from apps.forms import RunForm


class RunViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.response = Run().get(self.request)
        self.request_post = self.factory.post(
            '/',
            {'app': 'app-test', 'command': 'command-test'})
        self.request_post.session = {}
        self.response_mock = Mock()

    def test_should_require_login_to_run_command(self):
        assert issubclass(Run, LoginRequiredView)

    def test_run_should_render_expected_template(self):
        self.assertEqual('apps/run.html', self.response.template_name)

    def test_context_should_contain_form(self):
        self.assertIn('form', self.response.context_data.keys())

    def test_form_in_context_should_has_a_instance_of_RunForm(self):
        form = self.response.context_data.get('form')
        self.assertTrue(isinstance(form, RunForm))

    def test_get_request_run_url_should_return_404(self):
        response = self.client.get('/app/run/')
        self.assertNotEqual(404, response.status_code)

    @patch('requests.post')
    def test_post_with_app_and_command_sends_post(self, post):
        self.request_post.session = {'tsuru_token': 'tokentest'}
        Run().post(self.request_post)
        self.assertEqual(1, post.call_count)
        post.assert_called_with(
            '%s/apps/app-test/run' % settings.TSURU_HOST,
            data=u'command-test',
            headers={'authorization':
                     self.request_post.session['tsuru_token']})

    @patch('requests.post')
    def test_post_with_valid_app_and_command(self, post):
        self.response_mock.status_code = 200
        self.response_mock.content = "command runned"
        post.side_effect = Mock(return_value=self.response_mock)
        response = Run().post(self.request_post)
        self.assertEqual("command runned",
                         response.context_data.get('message'))
        self.assertIn('form', response.context_data.keys())
        self.assertTrue(isinstance(response.context_data.get('form'),
                                   RunForm))

    @patch('requests.post')
    def test_post_with_invalid_app_or_command_error_in_context(self, post):
        self.response_mock.status_code = 500
        self.response_mock.content = 'Error'
        post.side_effect = Mock(return_value=self.response_mock)
        response = Run().post(self.request_post)
        self.assertEqual('Error', response.context_data.get('errors'))

    @patch('requests.post')
    def test_post_with_invalid_app_or_command(self, post):
        self.response_mock.status_code = 500
        self.response_mock.content = 'Error'
        post.side_effect = Mock(return_value=self.response_mock)
        response = Run().post(self.request_post)
        self.assertIn('form', response.context_data.keys())
        self.assertTrue(isinstance(response.context_data.get('form'),
                                   RunForm))

    @patch('requests.post')
    def test_post_without_app_should_not_send_request_to_tsuru(self, post):
            request = self.factory.post('/', {'app': '',
                                              'command': 'comand-test'})
            request.session = {}
            Run().post(request)
            self.assertEqual(0, post.call_count)

    @patch('requests.post')
    def test_post_without_app_should_return_form_with_errors(self, post):
        request = self.factory.post('/', {'app': '',
                                          'command': 'command-test'})
        request.session = {}
        response = Run().post(request)
        self.assertIn('form', response.context_data.keys())
        form = response.context_data.get('form')
        self.assertTrue(isinstance(form, RunForm))
        self.assertEqual(u'This field is required.',
                         form.errors.get('app')[0])
