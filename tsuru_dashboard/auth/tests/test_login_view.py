from django.http import HttpResponseRedirect
from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from mock import Mock, patch

import httpretty

from tsuru_dashboard import settings
from tsuru_dashboard.auth.forms import LoginForm
from tsuru_dashboard.auth.views import Login


class LoginViewTest(TestCase):
    def setUp(self):
        httpretty.enable()
        url = "{}/users/info".format(settings.TSURU_HOST)
        httpretty.register_uri(httpretty.GET, url, status=200, body='{"Permissions": []}')

    @patch("requests.get")
    def test_login_get(self, get_mock):
        request = RequestFactory().get("/")
        request.session = {"next_url": "/"}
        response = Login.as_view()(request)
        self.assertIn("auth/login.html", response.template_name)
        form = response.context_data["form"]
        self.assertIsInstance(form, LoginForm)

    @patch("requests.get")
    def test_should_validate_data_from_post(self, get_mock):
        data = {"username": "invalid name", "password": ""}
        request = RequestFactory().post("/", data)
        request.session = {"next_url": "/"}
        response = Login.as_view()(request)
        form = response.context_data["form"]
        self.assertIn("auth/login.html", response.template_name)
        self.assertIsInstance(form, LoginForm)
        self.assertEqual("invalid name", form.data["username"])

    @patch("requests.post")
    @patch("requests.get")
    def test_should_return_invalid_message_when_user_doesnt_exist(self, get_mock, post):
        data = {"username": "invalid@email.com", "password": "123456"}
        post.return_value = Mock(status_code=500, content="user doesn't exist")
        response = self.client.post(reverse("login"), data, follow=True)
        error = response.context_data["form"].errors["__all__"]
        self.assertEqual(["user doesn't exist"], error)

    @patch("requests.post")
    @patch("requests.get")
    def test_should_send_request_post_to_tsuru_with_args_expected(self, get_mock, post):
        data = {"username": "valid@email.com", "password": "123456"}
        request = RequestFactory().post("/", data)
        request.session = {"next_url": "/"}
        expected_url = "%s/users/valid@email.com/tokens" % settings.TSURU_HOST
        Login.as_view()(request)
        self.assertEqual(1, post.call_count)
        post.assert_called_with(expected_url,
                                data='{"password": "123456"}')

    @patch("requests.post")
    def test_should_set_token_in_the_session(self, post):
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = {"token": "my beautiful token"}
        post.return_value = response_mock
        data = {"username": "valid@email.com", "password": "123456"}
        request = RequestFactory().post("/", data)
        request.session = {}
        Login.as_view()(request)
        self.assertEqual("type my beautiful token", request.session["tsuru_token"])

    @patch("requests.post")
    def test_set_admin_permission_in_session(self, post):
        url = "{}/users/info".format(settings.TSURU_HOST)
        httpretty.register_uri(
            httpretty.GET, url, status=200, body='{"Permissions": [{"Name": "", "ContextType": "global"}]}'
        )
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = {"token": "my beautiful token"}
        post.return_value = response_mock
        data = {"username": "valid@email.com", "password": "123456"}
        request = RequestFactory().post("/", data)
        request.session = {}
        Login.as_view()(request)
        self.assertDictEqual({"healing": True, "admin": True}, request.session["permissions"])

    @patch("requests.post")
    def test_set_healing_permission_in_session(self, post):
        url = "{}/users/info".format(settings.TSURU_HOST)
        httpretty.register_uri(
            httpretty.GET, url, status=200, body='{"Permissions": [{"Name": "healing.read"}]}'
        )
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = {"token": "my beautiful token"}
        post.return_value = response_mock
        data = {"username": "valid@email.com", "password": "123456"}
        request = RequestFactory().post("/", data)
        request.session = {}
        Login.as_view()(request)
        self.assertDictEqual({"healing": True, "admin": False}, request.session["permissions"])

    @patch("requests.post")
    def test_should_set_username_in_the_session(self, post):
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = {"token": "my beautiful token"}
        post.return_value = response_mock
        data = {"username": "valid@email.com", "password": "123456"}
        request = RequestFactory().post("/", data)
        request.session = {}
        Login.as_view()(request)
        self.assertEqual(data["username"], request.session["username"])

    @patch("requests.post")
    def test_redirect_to_team_creation_when_login_is_successful(self, post):
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = {"token": "my beautiful token"}
        post.return_value = response_mock
        data = {"username": "valid@email.com", "password": "123456"}
        request = RequestFactory().post("/", data)
        request.session = {}
        response = Login.as_view()(request)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual("/apps", response["Location"])

    @patch("requests.post")
    def test_redirect_to_team_creation_settings_false(self, post):
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = {"token": "my beautiful token"}
        post.return_value = response_mock
        data = {"username": "valid@email.com", "password": "123456"}
        request = RequestFactory().post("/", data)
        request.session = {}
        response = Login.as_view()(request)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual("/apps", response["Location"])

    @patch("requests.post")
    def test_redirect_to_apps(self, post):
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = {"token": "my beautiful token"}
        post.return_value = response_mock
        data = {"username": "valid@email.com", "password": "123456"}
        request = RequestFactory().post("/", data)
        request.session = {}
        response = Login.as_view()(request)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual("/apps", response["Location"])

    @patch("requests.get")
    def test_scheme_info(self, get_mock):
        view = Login()
        expected_url = "{}/auth/scheme".format(settings.TSURU_HOST)

        self.assertDictEqual(view.scheme_info(), {})
        get_mock.assert_called_with(expected_url)

        response_mock = Mock(status_code=200)
        response_mock.json.return_value = {"name": "oauth"}
        get_mock.return_value = response_mock

        self.assertDictEqual(view.scheme_info(), {"name": "oauth"})

        get_mock.assert_called_with(expected_url)

    @patch("requests.get")
    def test_get_context_data(self, get_mock):
        request = RequestFactory().get("/")
        request.session = {"next_url": "/"}
        request.META["HTTP_HOST"] = "localhost:3333"
        view = Login()
        view.request = request

        response_mock = Mock(status_code=200)
        response_mock.json.return_value = {
            "name": "oauth",
            "data": {
                "authorizeUrl":
                "http://something.com/?redirect=__redirect_url__"
            }
        }
        get_mock.return_value = response_mock

        data = view.get_context_data()

        self.assertDictEqual(data["scheme_info"], {
            "name": "oauth",
            "data": {
                "authorizeUrl":
                "http://something.com/?redirect=__redirect_url__"
            },
        })
        self.assertEqual(
            data["authorize_url"],
            "http://something.com/?redirect=http://localhost:3333/auth/callback/"
        )

    @patch("requests.get")
    def test_get_context_data_with_data_is_none(self, get_mock):
        request = RequestFactory().get("/")
        request.META["HTTP_HOST"] = "localhost:3333"
        request.session = {"next_url": "/"}
        view = Login()
        view.request = request

        response_mock = Mock(status_code=200)
        response_mock.json.return_value = {
            "name": "native",
            "data": None
        }
        get_mock.return_value = response_mock

        data = view.get_context_data()

        self.assertDictEqual(data["scheme_info"], {
            "name": "native",
            "data": None,
        })
