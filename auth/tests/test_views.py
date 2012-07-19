from django.test import TestCase
from django.test.client import RequestFactory

from auth.views import login


class LoginViewTest(TestCase):
    def test_login_expected_template_view(self):
        request = RequestFactory().get('/')
        response = login(request)
        self.assertEqual('auth/login.html', response.template_name)
