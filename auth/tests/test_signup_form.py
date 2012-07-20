from django.utils.unittest import TestCase

from auth import forms


class SignupFormTest(TestCase):
    def test_signup_form_should_have_email_password_and_same_password_again_fields(self):
        self.assertIn('email', forms.SignupForm.base_fields)
        self.assertIn('password', forms.SignupForm.base_fields)
        self.assertIn('same_password_again', forms.SignupForm.base_fields)

    def test_password_and_same_password_again_should_have_same_text(self):
        data = {'email':'test@test.com', 'password':'abc123', 'same_password_again': 'abc123'}
        form = forms.SignupForm(data)
        self.assertTrue(form.is_valid())

    def test_shuld_show_an_error_if_password_and_same_password_again_should_are_not_the_same(self):
        data = {'email':'test@test.com', 'password':'abc123', 'same_password_again': 'not the same'}
        form = forms.SignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn(u'You must type the same password twice!', form.errors['same_password_again'])