from django.test import TestCase

from tsuru_dashboard.auth import forms


class SignupFormTest(TestCase):
    def test_fields(self):
        self.assertIn('email', forms.SignupForm.base_fields)
        self.assertIn('password', forms.SignupForm.base_fields)
        self.assertIn('same_password_again', forms.SignupForm.base_fields)

    def test_password_confirmation_is_valid(self):
        data = {'email': 'test@test.com', 'password': 'abc123',
                'same_password_again': 'abc123'}
        form = forms.SignupForm(data)
        self.assertTrue(form.is_valid())

    def test_password_confirmation_is_invalid(self):
        data = {'email': 'test@test.com', 'password': 'abc123',
                'same_password_again': 'not the same'}
        form = forms.SignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn(u'You must type the same password twice!',
                      form.errors['same_password_again'])
