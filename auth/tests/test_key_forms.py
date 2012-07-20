from django.utils.unittest import TestCase
from django.forms import CharField

from auth import forms


class KeyFormTest(TestCase):
    def test_forms_should_have_KeyForm(self):
        self.assertTrue(hasattr(forms, 'KeyForm'))

    def test_team_should_have_key_field(self):
        self.assertIn('key', forms.KeyForm.base_fields)

    def test_key_should_has_a_CharField(self):
        field = forms.KeyForm.base_fields['key']
        self.assertTrue(isinstance(field, CharField))

    def test_key_should_have_at_most_2000_characters(self):
        field = forms.KeyForm.base_fields['key']
        self.assertEqual(2000, field.max_length)
