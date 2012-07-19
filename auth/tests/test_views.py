from mock import patch, Mock

from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory
from django.http import Http404

from auth.views import Login, Team, Signup
from auth.forms import TeamForm, LoginForm, SignupForm


class LoginViewTest(TestCase):
    def test_root_should_show_login_template(self):
        request = RequestFactory().get('/')
        response = Login().get(request)
        self.assertEqual('auth/login.html', response.template_name)

    def test_login_should_show_template(self):
        request = RequestFactory().get('/login')
        response = Login().get(request)
        self.assertEqual('auth/login.html', response.template_name)

    def test_login_form_should_be_in_the_view_context(self):
        request = RequestFactory().get('/')
        response = Login().get(request)
        form = response.context_data['login_form']
        self.assertIsInstance(form, LoginForm)

    def test_should_validate_data_from_post(self):
        data = {'username': 'invalid name', 'password': ''}
        request = RequestFactory().post('/', data)
        response = Login().post(request)
        form = response.context_data['login_form']

        self.assertEqual('auth/login.html', response.template_name)
        self.assertIsInstance(form, LoginForm)
        self.assertEqual('invalid name', form.data['username'])



class TeamViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.response = Team().get(self.request)
        self.response_mock = Mock()

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
        request = self.factory.post('/team/', {'name': 'test-team'})
        with patch('requests.post') as post:
            Team().post(request)
            self.assertEqual(1, post.call_count)
            post.assert_called_with('%s/teams' % settings.TSURU_HOST, {u'name': [u'test-team']})

    def test_post_with_valid_name_should_return_200(self):
        request = self.factory.post('/team/', {'name': 'test-team'})
        with patch('requests.post') as post:
            self.response_mock.status_code = 200
            post.side_effect = Mock(return_value=self.response_mock)
            response = Team().post(request)
            self.assertEqual(200, response.status_code)

    def test_post_with_invalid_name_should_return_500(self):
        request = self.factory.post('/team/', {'name': 'test-team'})
        with patch('requests.post') as post:
            self.response_mock.status_code = 500
            post.side_effect = Mock(return_value=self.response_mock)
            response = Team().post(request)
            self.assertEqual(500, response.status_code)

    def test_post_without_name_should_return_form_with_errors(self):
        request = self.factory.post('/team/', {'name': ''})
        response = Team().post(request)
        errors =  response.context_data.get('form').errors
        self.assertIn('name', errors)
        self.assertIn(u'This field is required.', errors.get('name'))


class SignupViewTest(TestCase):
    def test_signup_should_show_template(self):
        response = Signup().get(RequestFactory().get('/'))
        self.assertEqual('auth/signup.html', response.template_name)

    def test_context_should_contain_form(self):
        response = Signup().get(RequestFactory().get('/'))
        form = response.context_data['signup_form']
        self.assertIsInstance(form, SignupForm)

    def test_should_validate_data_from_post(self):
        data = {'email': '', 'password': '', 'same_password_again': ''}
        request = RequestFactory().post('/', data)
        response = Signup().post(request)
        form = response.context_data['signup_form']

        self.assertEqual(form.errors['email'][0], u'This field is required.')
        self.assertEqual(form.errors['password'][0], u'This field is required.')
        self.assertEqual(form.errors['same_password_again'][0], u'This field is required.')
