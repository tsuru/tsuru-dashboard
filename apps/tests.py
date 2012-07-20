from django.test import TestCase
from django.test.client import RequestFactory

from apps.views import CreateApp
from apps import forms


class AppFormTest(TestCase):

    def test_forms_should_have_AppForm(self):
        self.assertTrue(hasattr(forms, "AppForm"))

    def test_AppForm_should_have_name_field(self):
        self.assertIn("name", forms.AppForm.base_fields)


class CreateAppViewTest(TestCase):

    def test_should_use_create_template(self):
        request = RequestFactory().get("/")
        response = CreateApp().get(request)
        self.assertEqual("apps/create.html", response.template_name)

    def test_AppForm_should_be_in_context(self):
        request = RequestFactory().get("/")
        response = CreateApp().get(request)
        app_form = response.context_data['app_form']
        self.assertIsInstance(app_form, forms.AppForm)
