from django.test import TestCase
from django.test.client import RequestFactory

from auth.views import ChangePassword
from auth.forms import ChangePasswordForm


class TestResetPasswordView(TestCase):
    def test_get(self):
        request = RequestFactory().get("/")
        response = ChangePassword.as_view()(request)
        self.assertIn('auth/change_password.html',
                      response.template_name)
        self.assertIsInstance(response.context_data['form'],
                              ChangePasswordForm)
