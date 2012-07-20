from mock import patch, Mock

from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory
from django.http import Http404

from auth.views import LoginRequiredView, Team
from auth.forms import TeamForm


class TeamViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.response = Team().get(self.request)
        self.request_post = self.factory.post('/team/', {'name': 'test-team'})
        self.request_post.session = {}
        self.response_mock = Mock()

    def test_should_require_login_to_create_team(self):
        assert issubclass(Team, LoginRequiredView)

    def test_team_should_render_expected_template(self):
        self.assertEqual('auth/team.html', self.response.template_name)

    def test_context_should_contain_form(self):
        self.assertIn('form', self.response.context_data.keys())

    def test_form_in_context_should_has_a_instance_of_TeamForm(self):
        form = self.response.context_data.get('form')
        self.assertTrue(isinstance(form, TeamForm))

    def test_get_request_team_url_should_return_200(self):
        try:
            self.client.get('/team/')
        except Http404:
            assert False

    def test_post_with_name_should_send_request_post_to_tsuru_with_args_expected(self):
        self.request_post.session = {'tsuru_token': 'tokentest'}
        with patch('requests.post') as post:
            Team().post(self.request_post)
            self.assertEqual(1, post.call_count)
            post.assert_called_with('%s/teams' % settings.TSURU_HOST,
                                    data='{"name": "test-team"}',
                                    headers={'authorization': self.request_post.session['tsuru_token']})

    def test_post_with_valid_name_should_return_context_with_message_expected(self):
        with patch('requests.post') as post:
            self.response_mock.status_code = 200
            post.side_effect = Mock(return_value=self.response_mock)
            response = Team().post(self.request_post)
            self.assertEqual("Team was successfully created", response.context_data.get('message'))

    def test_post_with_invalid_name_should_return_500(self):
        with patch('requests.post') as post:
            self.response_mock.status_code = 500
            self.response_mock.content = 'Error'
            post.side_effect = Mock(return_value=self.response_mock)
            response = Team().post(self.request_post)
            self.assertEqual('Error', response.context_data.get('errors'))

    def test_post_without_name_should_return_form_with_errors(self):
        request = self.factory.post('/team/', {'name': ''})
        request.session = {}
        response = Team().post(request)
        form =  response.context_data.get('form')
        self.assertIn('name', form.errors)
        self.assertIn(u'This field is required.', form.errors.get('name'))
