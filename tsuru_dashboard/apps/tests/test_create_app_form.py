from django.test import TestCase

from tsuru_dashboard.apps import forms


class AppFormTest(TestCase):

    def test_forms_should_have_AppForm(self):
        self.assertTrue(hasattr(forms, "AppForm"))

    def test_fields(self):
        fields = ["name", "platform", "teamOwner", "pool", "plan"]
        for field_name in fields:
            self.assertIn(field_name, forms.AppForm.base_fields)

    def test_required_false_fields(self):
        fields = ["teamOwner", "pool", "plan"]
        for field_name in fields:
            self.assertFalse(forms.AppForm.base_fields[field_name].required)

    def test_required_fields(self):
        fields = ["name", "platform"]
        for field_name in fields:
            self.assertTrue(forms.AppForm.base_fields[field_name].required)
