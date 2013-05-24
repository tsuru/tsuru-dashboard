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

    def test_old_is_required(self):
        data = {
            "new": "new",
            "confirm": "new",
        }
        form = ChangePasswordForm(data)
        self.assertFalse(form.is_valid())

    def test_new_is_required(self):
        data = {
            "old": "old",
            "confirm": "new",
        }
        form = ChangePasswordForm(data)
        self.assertFalse(form.is_valid())

    def test_confirm_is_required(self):
        data = {
            "old": "old",
            "new": "new",
        }
        form = ChangePasswordForm(data)
        self.assertFalse(form.is_valid())
