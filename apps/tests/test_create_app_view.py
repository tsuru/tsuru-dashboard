import json

from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory
from django.conf import settings

from apps.views import CreateApp
from apps import forms


class CreateAppViewTest(TestCase):

    @patch('requests.get')
    def test_should_use_create_template(self, get):
        content = u"""[{"Name":"python"},{"Name":"ruby"},{"Name":"static"}]"""
        m = Mock(status_code=200, content=content)
        m.json.return_value = json.loads(content)
        get.return_value = m
        request = RequestFactory().get("/")
        request.session = {}

        view = CreateApp()
        view.plans = lambda r: ("small", [("small", "small")])
        view.teams = lambda r: []
        view.pools = lambda r: []
        response = view.get(request)

        self.assertEqual("apps/create.html", response.template_name)

    @patch('requests.get')
    def test_AppForm_should_be_in_context(self, get):
        content = u"""[{"Name":"python"},{"Name":"ruby"},{"Name":"static"}]"""
        m = Mock(status_code=200, content=content)
        m.json.return_value = json.loads(content)
        get.return_value = m
        request = RequestFactory().get("/")
        request.session = {}

        view = CreateApp()
        view.plans = lambda r: ("basic", [("basic", "basic")])
        view.teams = lambda r: []
        view.pools = lambda r: []
        response = view.get(request)

        app_form = response.context_data['app_form']
        self.assertIsInstance(app_form, forms.AppForm)

    @patch('requests.get')
    @patch('requests.post')
    def test_post_with_invalid_name_should_return_500(self, post, get):
        content = u"""[{"Name":"python"},{"Name":"ruby"},{"Name":"static"}]"""
        m = Mock(status_code=200, content=content)
        m.json.return_value = json.loads(content)
        get.return_value = m
        request = RequestFactory().post(
            "/",
            {"name": "myepe", "platform": "python"})
        request.session = {}
        post.return_value = Mock(status_code=500, content='Error')

        view = CreateApp()
        view.plans = lambda r: ("small", [("small", "small")])
        view.teams = lambda r: []
        view.pools = lambda r: []
        response = view.post(request)

        self.assertEqual('Error', response.context_data.get("errors"))

    @patch('requests.get')
    def test_post_without_name_should_return_form_with_errors(self, get):
        content = u"""[{"Name":"python"},{"Name":"ruby"},{"Name":"static"}]"""
        m = Mock(status_code=200, content=content)
        m.json.return_value = json.loads(content)
        get.return_value = m
        request = RequestFactory().post("/", {"name": ""})
        request.session = {}

        view = CreateApp()
        view.plans = lambda r: ("small", [("small", "small")])
        view.teams = lambda r: []
        view.pools = lambda r: []
        response = view.post(request)

        form = response.context_data.get('app_form')
        self.assertIn('name', form.errors)
        self.assertIn(u'This field is required.', form.errors.get('name'))

    @patch('requests.get')
    @patch('requests.post')
    def test_post_should_send_to_tsuru_with_args_expected(self, post, get):
        post.return_value = Mock(status_code=200)

        data = {"name": "myepe", "platform": "django", "plan": "basic"}
        request = RequestFactory().post("/", data)
        request.session = {'tsuru_token': 'tokentest'}

        view = CreateApp()
        view.plans = lambda r: ("basic", [("basic", "basic")])
        view.platforms = lambda r: [("django", "django")]
        view.post(request)

        self.assertEqual(1, post.call_count)
        url = '{}/apps'.format(settings.TSURU_HOST)
        post.assert_called_with(
            url,
            data='{"platform": "django", "name": "myepe", "plan": {"name": "basic"}}',
            headers={'authorization': request.session['tsuru_token']}
        )
