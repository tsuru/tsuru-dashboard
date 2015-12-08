from django.test import TestCase

from tsuru_dashboard import settings
from tsuru_dashboard.auth.forms import TokenRequestForm

from mock import patch, Mock


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

    @patch("requests.post")
    @patch("requests.get")
    def test_send_request(self, get, post):
        get.return_value = Mock(status_code=200)
        form = TokenRequestForm({"email": "a@a.com"})
        form.is_valid()
        form.send()
        url = "{0}/users/{1}/password".format(settings.TSURU_HOST,
                                              form.cleaned_data["email"])
        post.assert_called_with(url)
