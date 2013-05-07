from django.test import TestCase

from apps import forms


class AppFormTest(TestCase):

    def test_forms_should_have_AppForm(self):
        self.assertTrue(hasattr(forms, "AppForm"))

    def test_AppForm_should_have_name_field(self):
        self.assertIn("name", forms.AppForm.base_fields)

    def test_AppForm_should_have_platform_field(self):
        self.assertIn("platform", forms.AppForm.base_fields)
