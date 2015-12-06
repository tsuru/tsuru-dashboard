from django.test import TestCase
from django.forms import CharField

from tsuru_dashboard.services import forms


class ServiceFormTest(TestCase):
    def test_forms_should_contains_ServiceForm(self):
        self.assertTrue(hasattr(forms, 'ServiceForm'))

    def test_should_have_name_field(self):
        self.assertIn('name', forms.ServiceForm.base_fields)

    def test_name_field_should_have_CharField(self):
        field = forms.ServiceForm.base_fields['name']
        self.assertIsInstance(field, CharField)

    def test_name_field_should_have_at_most_50_characters(self):
        field = forms.ServiceForm.base_fields['name']
        self.assertEqual(50, field.max_length)
