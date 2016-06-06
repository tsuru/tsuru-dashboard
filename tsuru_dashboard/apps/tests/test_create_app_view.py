import json

from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory

from tsuru_dashboard import settings
from tsuru_dashboard.apps.views import CreateApp
from tsuru_dashboard.apps import forms


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

    @patch("django.contrib.messages.error")
    @patch('requests.get')
    @patch('requests.post')
    def test_post_with_invalid_name_should_return_500(self, post, get, error):
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

        view.post(request)

        error.assert_called_with(request, u'Error', fail_silently=True)

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
            data={"platform": "django", "name": "myepe", "plan": "basic"},
            headers={'authorization': request.session['tsuru_token']}
        )

    @patch('requests.get')
    @patch('requests.post')
    def test_post_should_send_to_tsuru_removing_empty_keys(self, post, get):
        post.return_value = Mock(status_code=200)

        data = {"name": "myepe", "platform": "django", "plan": ""}
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
            data={"platform": "django", "name": "myepe"},
            headers={'authorization': request.session['tsuru_token']}
        )

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
