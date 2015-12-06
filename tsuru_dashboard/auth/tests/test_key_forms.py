from django.test import TestCase
from django.forms import CharField, Textarea

from tsuru_dashboard.auth import forms


class KeyFormTest(TestCase):
    def test_forms_should_have_KeyForm(self):
        self.assertTrue(hasattr(forms, 'KeyForm'))

    def test_should_have_key_field(self):
        self.assertIn('key', forms.KeyForm.base_fields)

    def test_key_should_has_a_CharField(self):
        field = forms.KeyForm.base_fields['key']
        self.assertIsInstance(field, CharField)

    def test_should_have_name_field(self):
        self.assertIn('name', forms.KeyForm.base_fields)

    def test_name_should_has_a_CharField(self):
        field = forms.KeyForm.base_fields['name']
        self.assertIsInstance(field, CharField)

    def test_key_should_be_a_TextArea(self):
        field = forms.KeyForm.base_fields['key']
        self.assertIsInstance(field.widget, Textarea)
