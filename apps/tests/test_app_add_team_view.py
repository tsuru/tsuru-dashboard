from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory
from django.conf import settings
from django.http import Http404

from apps.views import AppAddTeam
from auth.views import LoginRequiredView
from apps.forms import AppAddTeamForm


class AppAddTeamTestCas(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.response = AppAddTeam().get(self.request)
        self.request_post = self.factory.post('/', {'app': 'app-test', 'team': 'team-test'})
        self.request_post.session = {}
        self.response_mock = Mock()

    def test_should_require_login_to_add_team_to_app(self):
        assert issubclass(AppAddTeam, LoginRequiredView)

    def test_should_render_expected_template(self):
        self.assertEqual('apps/app_add_team.html', self.response.template_name)

    def test_context_should_contain_form(self):
        self.assertIn('form', self.response.context_data.keys())

    def test_form_in_context_should_has_a_instance_of_AppAddTeamForm(self):
        form = self.response.context_data.get('form')
        self.assertTrue(isinstance(form, AppAddTeamForm))

    def test_get_request_team_url_should_return_200(self):
        try:
            self.client.get('/app/team/add')
        except Http404:
            assert False

    def test_post_app_and_team_should_send_request_post_to_tsuru_with_args_expected(self):
        self.request_post.session = {'tsuru_token': 'tokentest'}
        with patch('requests.put') as put:
            AppAddTeam().post(self.request_post)
            self.assertEqual(1, put.call_count)
            put.assert_called_with('%s/apps/app-test/team-test' % settings.TSURU_HOST,
                                    headers={'authorization': self.request_post.session['tsuru_token']})

    def test_post_with_valid_and_team_should_return_context_with_message_expected(self):
        with patch('requests.put') as put:
            self.response_mock.status_code = 200
            put.side_effect = Mock(return_value=self.response_mock)
            response = AppAddTeam().post(self.request_post)
            self.assertEqual("The Team was successfully added", response.context_data.get('message'))

    def test_post_with_invalid_app_or_team_should_return_error_message_expected_on_context(self):
        with patch('requests.put') as put:
            self.response_mock.status_code = 500
            self.response_mock.content = 'Error'
            put.side_effect = Mock(return_value=self.response_mock)
            response = AppAddTeam().post(self.request_post)
            self.assertEqual('Error', response.context_data.get('errors'))

    def test_post_with_valid_data_should_return_context_with_form(self):
        with patch('requests.put') as put:
            self.response_mock.status_code = 200
            put.side_effect = Mock(return_value=self.response_mock)
            response = AppAddTeam().post(self.request_post)
            self.assertIn('form', response.context_data.keys())
            self.assertTrue(isinstance(response.context_data.get('form'), AppAddTeamForm))

    def test_post_with_invalid_data_should_return_context_with_form(self):
        with patch('requests.put') as put:
            self.response_mock.status_code = 500
            self.response_mock.content = 'Error'
            put.side_effect = Mock(return_value=self.response_mock)
            response = AppAddTeam().post(self.request_post)
            self.assertIn('form', response.context_data.keys())
            self.assertTrue(isinstance(response.context_data.get('form'), AppAddTeamForm))

    def test_post_with_invalid_form_should_not_send_request_to_tsuru(self):
        with patch('requests.put') as put:
            request = self.factory.post('/', {'app': 'app-test', 'team': ''})
            request.session = {}
            AppAddTeam().post(request)
            self.assertEqual(0, put.call_count)

    def test_post_with_invalid_form_should_return_form_with_errors(self):
        with patch('requests.put'):
            request = self.factory.post('/', {'app': 'app-test', 'team': ''})
            request.session = {}
            response = AppAddTeam().post(request)
            self.assertIn('form', response.context_data.keys())
            form = response.context_data.get('form')
            self.assertTrue(isinstance(form, AppAddTeamForm))
            self.assertEqual(u'This field is required.', form.errors.get('team')[0])
