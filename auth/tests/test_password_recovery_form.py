from django.test import TestCase

from auth.forms import PasswordRecoveryForm


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
