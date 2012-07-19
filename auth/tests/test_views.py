from django.test import TestCase
from django.test.client import RequestFactory

from auth.views import login
from auth.forms import LoginForm


class LoginViewTest(TestCase):
    def test_login_expected_template_view(self):
        request = RequestFactory().get('/')
        response = login(request)
        self.assertEqual('auth/login.html', response.template_name)

    def test_login_form_should_be_in_the_view_context(self):
        request = RequestFactory().get('/')
        response = login(request)
        form = response.context_data['login_form']
        self.assertIsInstance(form, LoginForm)