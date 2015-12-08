from django.test import TestCase

from tsuru_dashboard import settings
from tsuru_dashboard.auth.forms import PasswordRecoveryForm

from mock import patch


class PasswordRecoveryFormTest(TestCase):
    def test_email_is_required(self):
        form = PasswordRecoveryForm({"token": "token"})
        self.assertFalse(form.is_valid())

    def test_token_is_required(self):
        form = PasswordRecoveryForm({"email": "a@a.com"})
        self.assertFalse(form.is_valid())

    def test_email_should_be_an_email(self):
        invalid_emails = ["a", "a@a", "a@a."]

        for email in invalid_emails:
            form = PasswordRecoveryForm({"email": email, "token": "token"})
            self.assertFalse(form.is_valid())

    def test_valid(self):
        form = PasswordRecoveryForm({"email": "a@a.com", "token": "token"})
        self.assertTrue(form.is_valid())

    @patch("requests.post")
    def test_send(self, post):
        form = PasswordRecoveryForm({"email": "a@a.com", "token": "token"})
        form.is_valid()
        form.send()
        url = "{0}/users/{1}/password?token={2}".format(
            settings.TSURU_HOST,
            form.cleaned_data["email"],
            form.cleaned_data["token"]
        )
        post.assert_called_with(url)
