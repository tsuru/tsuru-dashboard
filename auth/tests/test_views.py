from django.test import TestCase
from django.test.client import RequestFactory

from auth.views import login, signup
from auth.forms import LoginForm

class LoginViewTest(TestCase):
    def test_root_should_show_login_template(self):
        request = RequestFactory().get('/')
        response = login(request)
        self.assertEqual('auth/login.html', response.template_name)

    def test_login_should_show_template(self):
        request = RequestFactory().get('/login')
        response = login(request)
        self.assertEqual('auth/login.html', response.template_name)

    def test_login_form_should_be_in_the_view_context(self):
        request = RequestFactory().get('/')
        response = login(request)
        form = response.context_data['login_form']
        self.assertIsInstance(form, LoginForm)


class SignUpViewTest(TestCase):
    def test_signup_should_show_template(self):
        request = RequestFactory().get('/signup')
        response = signup(request)
        self.assertEqual('auth/signup.html', response.template_name)


