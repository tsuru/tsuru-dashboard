from mock import patch, Mock

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

    def test_post_with_invalid_name_should_return_500(self):
        request = RequestFactory().post("/", {"name": "myepe"})
        request.session = {}
        response_mock = Mock()
        with patch('requests.post') as post:
            response_mock.status_code = 500
            response_mock.content = 'Error'
            post.side_effect = Mock(return_value=response_mock)
            response = CreateApp().post(request)
            self.assertEqual('Error', response.context_data.get('msg'))

    def test_post_without_name_should_return_form_with_errors(self):
        request = RequestFactory().post("/", {"name": ""})
        request.session = {}
        response = CreateApp().post(request)
        form =  response.context_data.get('form')
        self.assertIn('name', form.errors)
        self.assertIn(u'This field is required.', form.errors.get('name'))
