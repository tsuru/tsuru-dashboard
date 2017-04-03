import json

from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory

from tsuru_dashboard.apps.views import CreateApp
from tsuru_dashboard.apps import forms
from tsuruclient.base import TsuruAPIError


class FakeTsuruClient(object):
    def __init__(self, exception=False, return_value=""):
        attrs = {}
        if exception:
            attrs["create.side_effect"] = TsuruAPIError(return_value)
        else:
            attrs["create.return_value"] = return_value
        self.apps = Mock(**attrs)


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

    @patch.object(CreateApp, "client", FakeTsuruClient(exception=True, return_value="Error creating app"))
    @patch("django.contrib.messages.error")
    @patch('requests.get')
    def test_post_with_errors_should_show_error_message(self, get, error):
        content = u"""[{"Name":"python"},{"Name":"ruby"},{"Name":"static"}]"""
        m = Mock(status_code=200, content=content)
        m.json.return_value = json.loads(content)
        get.return_value = m
        request = RequestFactory().post(
            "/",
            {"name": "myepe", "platform": "python"})
        request.session = {}

        view = CreateApp()
        view.plans = lambda r: ("small", [("small", "small")])
        view.teams = lambda r: []
        view.pools = lambda r: []

        view.post(request)

        error.assert_called_with(request, u'Error creating app', fail_silently=True)

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

    @patch.object(CreateApp, "client", FakeTsuruClient())
    @patch('requests.get')
    def test_post_should_send_to_tsuru_removing_empty_keys(self, get):
        data = {"name": "myepe", "platform": "django", "plan": ""}
        request = RequestFactory().post("/", data)
        request.session = {'tsuru_token': 'tokentest'}

        view = CreateApp()
        view.plans = lambda r: ("basic", [("basic", "basic")])
        view.platforms = lambda r: [("django", "django")]
        view.post(request)

        CreateApp.client.apps.create.assert_called_with(name="myepe", platform="django")

    @patch.object(CreateApp, "client", FakeTsuruClient())
    @patch('requests.get')
    def test_post_should_split_tags(self, get):
        data = {"name": "myepe", "platform": "django", "tags": " tag 1 , tag 2, tag 3  ,, , "}
        request = RequestFactory().post("/", data)
        request.session = {'tsuru_token': 'tokentest'}

        view = CreateApp()
        view.plans = lambda r: ("basic", [("basic", "basic")])
        view.platforms = lambda r: [("django", "django")]
        view.post(request)

        CreateApp.client.apps.create.assert_called_with(name="myepe", platform="django", tag=["tag 1", "tag 2", "tag 3"])

    @patch.object(CreateApp, "client", FakeTsuruClient())
    @patch("django.contrib.messages.success")
    @patch('requests.get')
    def test_post_with_success_should_redirect_to_app_list(self, get, success):
        data = {"name": "myepe", "platform": "django", "plan": ""}
        request = RequestFactory().post("/", data)
        request.session = {'tsuru_token': 'tokentest'}

        view = CreateApp()
        view.plans = lambda r: ("basic", [("basic", "basic")])
        view.platforms = lambda r: [("django", "django")]
        response = view.post(request)

        success.assert_called_with(request, u'App was successfully created', fail_silently=True)
        self.assertEquals(302, response.status_code)
        self.assertEquals("/apps/", response.url)

    @patch('requests.get')
    def test_pools_old_format(self, get):
        content = u"""[{"Pools": ["basic", "one"], "Team": "andrews"}]"""
        m = Mock(status_code=200, content=content)
        m.json.return_value = json.loads(content)
        get.return_value = m
        request = RequestFactory().get("/")
        request.session = {'tsuru_token': 'tokentest'}

        view = CreateApp()
        pools = view.pools(request)
        self.assertListEqual([("", ""), ('one', 'one'), ('basic', 'basic')], pools)

    @patch('requests.get')
    def test_pools_1_0(self, get):
        content = u"""[{"Name": "dead"}]"""
        m = Mock(status_code=200, content=content)
        m.json.return_value = json.loads(content)
        get.return_value = m
        request = RequestFactory().get("/")
        request.session = {'tsuru_token': 'tokentest'}

        view = CreateApp()
        pools = view.pools(request)
        self.assertListEqual([("", ""), ('dead', 'dead')], pools)

    @patch("requests.get")
    def test_pools_empty(self, get):
        content = u"[]"
        m = Mock(status_code=200, content=content)
        m.json.return_value = json.loads(content)
        get.return_value = m
        request = RequestFactory().get("/")
        request.session = {'tsuru_token': 'tokentest'}

        view = CreateApp()
        pools = view.pools(request)
        self.assertListEqual([('', '')], pools)

    @patch('requests.get')
    def test_pools_new_api(self, get):
        content = u"""{"pools_by_team": [{"Pools": ["one"], "Team": "admin"}],
            "public_pools": [{"Default": "True", "Public": "True", "Name": "basic", "Teams": []}]}"""
        m = Mock(status_code=200, content=content)
        m.json.return_value = json.loads(content)
        get.return_value = m
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "tokentest"}

        view = CreateApp()
        pools = view.pools(request)
        self.assertEqual([("", ""), ('one', 'one'), ('basic', 'basic')], pools)

    @patch('requests.get')
    def test_teams(self, get):
        content = u"""[{"name": "team1"}]"""
        m = Mock(status_code=200, content=content)
        m.json.return_value = json.loads(content)
        get.return_value = m
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "tokentest"}

        view = CreateApp()
        teams = view.teams(request)
        self.assertEqual([("", ""), ('team1', 'team1')], teams)

    @patch('requests.get')
    def test_teams_empty(self, get):
        m = Mock(status_code=204)
        get.return_value = m
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "tokentest"}

        view = CreateApp()
        teams = view.teams(request)
        self.assertEqual([("", "")], teams)

    @patch('requests.get')
    def test_plans(self, get):
        content = u"""[{"name": "plan1"}]"""
        m = Mock(status_code=200, content=content)
        m.json.return_value = json.loads(content)
        get.return_value = m
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "tokentest"}

        view = CreateApp()
        plans = view.plans(request)
        self.assertEqual(("", [("", ""), ('plan1', 'plan1')]), plans)

    @patch('requests.get')
    def test_plans_is_None(self, get_mock):
        response_mock = Mock()
        response_mock.json.return_value = None
        get_mock.return_value = response_mock

        data = {"name": "myepe", "platform": "django", "plan": "basic"}
        request = RequestFactory().post("/", data)
        request.session = {'tsuru_token': 'tokentest'}

        view = CreateApp()
        default, plans = view.plans(request)
        self.assertEqual(default, '')
        self.assertListEqual([('', '')], plans)
