from django.test import TestCase
from django.test.client import RequestFactory
from django.http import Http404

from auth.views import Login, team, Signup
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
        self.request = RequestFactory().get('/')
        self.response = team(self.request)

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


class SignUpViewTest(TestCase):
    def test_signup_should_show_template(self):
        request = RequestFactory().get('/signup')
        response = Signup().get(request)
        self.assertEqual('auth/signup.html', response.template_name)
 
    def test_context_should_contain_form(self):
        request = RequestFactory().get('/signup')
        response = Signup().get(request)
        form = response.context_data['signup_form']
        self.assertIsInstance(form, SignupForm)
