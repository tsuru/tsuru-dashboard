from django.test import TestCase
from django.test.client import RequestFactory
import mock

import json

from auth.views import Callback


class CallbackViewTest(TestCase):

    @mock.patch("requests.post")
    def test_callback(self, post_mock):
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
