from django.test import TestCase
from django.test.client import RequestFactory

import mock
import httpretty

import json

from tsuru_dashboard import settings
from tsuru_dashboard.auth.views import Callback


class CallbackViewTest(TestCase):

    @httpretty.activate
    @mock.patch("requests.post")
    def test_callback(self, post_mock):
        url = "{}/users/info".format(settings.TSURU_HOST)
        httpretty.register_uri(httpretty.GET, url, status=200, body='{"Permissions": []}')

        response_mock = mock.Mock(status_code=200)
        response_mock.json.return_value = {"token": "xpto"}

        post_mock.return_value = response_mock

        request = RequestFactory().get('/', {"code": "somecode"})
        request.META['HTTP_HOST'] = 'localhost:3333'
        request.session = {"next_url": "/apps"}

        response = Callback.as_view()(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/apps")

        self.assertEqual(request.session["tsuru_token"], "type xpto")
        self.assertDictEqual(request.session["permissions"], {"healing": False, "admin": False})

        expected_url = 'http://localhost:8080/auth/login'
        expected_data = json.dumps({
            "redirectUrl": "http://localhost:3333/auth/callback/",
            "code": "somecode"
        })

        post_mock.assert_called_with(expected_url, data=expected_data)

    @mock.patch("requests.post")
    def test_callback_wrong_status_code(self, post_mock):
        request = RequestFactory().get('/')
        request.META['HTTP_HOST'] = 'localhost:3333'

        response = Callback.as_view()(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/auth/login")

    @httpretty.activate
    @mock.patch("requests.post")
    def test_callback_with_permissions(self, post_mock):
        url = "{}/users/info".format(settings.TSURU_HOST)
        httpretty.register_uri(
            httpretty.GET, url, status=200,
            body='{"Permissions": [{"Name":"healing.read"}, {"Name": "", "ContextType": "global"}]}'
        )
        response_mock = mock.Mock(status_code=200)
        response_mock.json.return_value = {"token": "xpto"}

        post_mock.return_value = response_mock

        request = RequestFactory().get('/', {"code": "somecode"})
        request.META['HTTP_HOST'] = 'localhost:3333'
        request.session = {"next_url": "/apps"}

        response = Callback.as_view()(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/apps")

        self.assertEqual(request.session["tsuru_token"], "type xpto")
        self.assertDictEqual(request.session["permissions"], {"healing": True, "admin": True})

        expected_url = 'http://localhost:8080/auth/login'
        expected_data = json.dumps({
            "redirectUrl": "http://localhost:3333/auth/callback/",
            "code": "somecode"
        })

        post_mock.assert_called_with(expected_url, data=expected_data)
