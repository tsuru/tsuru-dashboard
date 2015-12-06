from django.test import TestCase
from django.forms import PasswordInput

from tsuru_dashboard.auth.forms import ChangePasswordForm


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

    def test_old_use_password_input(self):
        old_field = ChangePasswordForm.base_fields['old']
        self.assertIsInstance(old_field.widget, PasswordInput)

    def test_new_use_password_input(self):
        new_field = ChangePasswordForm.base_fields['new']
        self.assertIsInstance(new_field.widget, PasswordInput)

    def test_confirm_use_password_input(self):
        confirm_field = ChangePasswordForm.base_fields['confirm']
        self.assertIsInstance(confirm_field.widget, PasswordInput)
