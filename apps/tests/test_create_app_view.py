from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory
from django.conf import settings

from apps.views import CreateApp
from apps import forms


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

    @patch('requests.post')
    def test_post_with_invalid_name_should_return_500(self, post):
        request = RequestFactory().post(
            "/",
            {"name": "myepe", "platform": "python"})
        request.session = {}
        post.return_value = Mock(status_code=500, content='Error')
        response = CreateApp().post(request)
        self.assertEqual('Error', response.context_data.get("errors"))

    def test_post_without_name_should_return_form_with_errors(self):
        request = RequestFactory().post("/", {"name": ""})
        request.session = {}
        response = CreateApp().post(request)
        form = response.context_data.get('app_form')
        self.assertIn('name', form.errors)
        self.assertIn(u'This field is required.', form.errors.get('name'))

    @patch('requests.post')
    def test_post_should_send_to_tsuru_with_args_expected(self, post):
        request = RequestFactory().post(
            "/",
            {"name": "myepe", "platform": "django"})
        request.session = {'tsuru_token': 'tokentest'}
        CreateApp().post(request)
        self.assertEqual(1, post.call_count)
        post.assert_called_with(
            '%s/apps' % settings.TSURU_HOST,
            data='{"platform": "django", "name": "myepe"}',
            headers={'authorization': request.session['tsuru_token']}
        )

    @patch('requests.post')
    def test_invalid_post_returns_context_with_message_expected(self, post):
        request = RequestFactory().post(
            "/",
            {"name": "myepe", "platform": "python"})
        request.session = {}
        post.return_value = Mock(status_code=200)
        response = CreateApp().post(request)
        self.assertEqual("App was successfully created",
                         response.context_data.get('message'))
