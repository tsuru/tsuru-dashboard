from django.test import TestCase
from django.forms import CharField

from tsuru_dashboard.apps import forms


class RunFormTest(TestCase):
    def test_forms_should_contains_RunForm(self):
        self.assertTrue(hasattr(forms, 'RunForm'))

    def test_should_have_app_field(self):
        self.assertIn('app', forms.RunForm.base_fields)

    def test_app_field_should_have_CharField(self):
        field = forms.RunForm.base_fields['app']
        self.assertIsInstance(field, CharField)

    def test_app_field_should_have_at_most_60_characters(self):
        field = forms.RunForm.base_fields['app']
        self.assertEqual(60, field.max_length)

    def test_should_have_command_field(self):
        self.assertIn('command', forms.RunForm.base_fields)

    def test_command_field_should_have_CharField(self):
        field = forms.RunForm.base_fields['command']
        self.assertIsInstance(field, CharField)

    def test_command_field_should_have_at_most_1000_characters(self):
        field = forms.RunForm.base_fields['command']
        self.assertEqual(1000, field.max_length)
