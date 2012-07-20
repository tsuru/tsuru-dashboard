from django.test import TestCase
from django.test.client import RequestFactory

from apps.views import Apps
from apps import forms


class AppFormTest(TestCase):

    def test_forms_should_have_AppForm(self):
        self.assertTrue(hasattr(forms, "AppForm"))

    def test_AppForm_should_have_name_field(self):
        self.assertIn("name", forms.AppForm.base_fields)


class ViewTest(TestCase):

    def test_should_use_app_template(self):
        request = RequestFactory().get("/")
        response = Apps().get(request)
        self.assertEqual("apps/create.html", response.template_name)

