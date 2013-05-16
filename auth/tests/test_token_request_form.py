from django.test import TestCase
from auth.forms import TokenRequestForm


class TokenRequestFormTest(TestCase):

    def test_email_is_required(self):
        form = TokenRequestForm()
        self.assertFalse(form.is_valid())

        form = TokenRequestForm({"email": "a@a.com"})
        self.assertTrue(form.is_valid())

    def test_email_should_be_an_email(self):
        form = TokenRequestForm({"email": "a@a.com"})
        self.assertTrue(form.is_valid())

        invalid_emails = ["a", "a@a", "a@a."]

        for email in invalid_emails:
            form = TokenRequestForm({"email": email})
            self.assertFalse(form.is_valid())
