from django.utils.unittest import TestCase
from django.forms import EmailField, CharField
from django.forms.widgets import PasswordInput

from auth import forms


class TokenFormTest(TestCase):
    def test_forms_should_have_TokenForm(self):
        self.assertTrue(hasattr(forms, 'TokenForm'))

    def test_team_should_have_token_field(self):
        self.assertIn('token', forms.TokenForm.base_fields)

    def test_token_should_have_at_most_2000_characters(self):
        field = forms.TokenForm.base_fields['token']
        self.assertEqual(2000, field.max_length)
