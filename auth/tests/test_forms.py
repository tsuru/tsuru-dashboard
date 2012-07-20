from django.utils.unittest import TestCase
from django.forms import EmailField, CharField
from django.forms.widgets import PasswordInput

from auth import forms


class TeamFormTest(TestCase):
    def test_forms_should_have_TeamForm(self):
        self.assertTrue(hasattr(forms, 'TeamForm'))

    def test_team_should_have_name_field(self):
        self.assertIn('name', forms.TeamForm.base_fields)

    def test_name_field_should_instance_of_CharField(self):
        field = forms.TeamForm.base_fields['name']
        self.assertIsInstance(field, CharField)

    def test_name_should_have_at_most_60_characters(self):
        field = forms.TeamForm.base_fields['name']
        self.assertEqual(60, field.max_length)


class LoginFormTest(TestCase):
    def test_login_should_have_username_and_password_fields(self):
        self.assertIn('username', forms.LoginForm.base_fields)
        self.assertIn('password', forms.LoginForm.base_fields)

    def test_widget_for_password_field_should_be_password(self):
        field = forms.LoginForm.base_fields['password']
        self.assertIsInstance(field.widget, PasswordInput)

    def test_username_should_have_at_most_60_characters(self):
        field = forms.LoginForm.base_fields['username']
        self.assertEqual(60, field.max_length)

    def test_password_should_have_at_least_6_characters(self):
        field = forms.LoginForm.base_fields['password']
        self.assertEqual(6, field.min_length)

    def test_username_field_should_accept_only_email_values(self):
        field = forms.LoginForm.base_fields['username']
        self.assertIsInstance(field, EmailField)


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


class KeyFormTest(TestCase):
    def test_forms_should_have_KeyForm(self):
        self.assertTrue(hasattr(forms, 'KeyForm'))

    def test_team_should_have_key_field(self):
        self.assertIn('key', forms.KeyForm.base_fields)

    def test_key_should_have_at_most_2000_characters(self):
        field = forms.KeyForm.base_fields['key']
        self.assertEqual(2000, field.max_length)
