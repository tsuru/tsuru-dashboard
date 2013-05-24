from django.test import TestCase

from auth.forms import ChangePasswordForm


class ChangePasswordFormTest(TestCase):
    def test_form_is_valid(self):
        data = {
            "old": "old",
            "new": "new",
            "confirm": "new",
        }
        form = ChangePasswordForm(data)
        self.assertTrue(form.is_valid())
