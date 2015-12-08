from mock import patch

from django.test import TestCase
from django.test.client import RequestFactory

import httpretty

from tsuru_dashboard import settings
from tsuru_dashboard.admin.views import NodeAdd


class NodeAddViewTest(TestCase):
    def setUp(self):
        httpretty.enable()

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_view_register_false(self, token_is_valid):
        token_is_valid.return_value = True

        factory = RequestFactory()
        request = factory.post('/?register=false', data={"key": "value"})
        request.session = {'tsuru_token': 'tokentest'}

        url = "{}/docker/node".format(settings.TSURU_HOST)
        httpretty.register_uri(
            httpretty.POST,
            url,
            body="{}",
            status=200
        )

        response = NodeAdd.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn("register", httpretty.last_request().querystring)
        self.assertEqual("false", httpretty.last_request().querystring["register"][0])

    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_view_register_true(self, token_is_valid):
        token_is_valid.return_value = True

        factory = RequestFactory()
        request = factory.post('/?register=true', data={"key": "value"})
        request.session = {'tsuru_token': 'tokentest'}

        url = "{}/docker/node".format(settings.TSURU_HOST)
        httpretty.register_uri(
            httpretty.POST,
            url,
            body="{}",
            status=200
        )

        response = NodeAdd.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn("register", httpretty.last_request().querystring)
        self.assertEqual("true", httpretty.last_request().querystring["register"][0])
