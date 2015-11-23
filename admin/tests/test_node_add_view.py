from mock import patch

from django.test import TestCase
from django.test.client import RequestFactory
from django.conf import settings

import httpretty

from admin.views import NodeAdd


class NodeAddViewTest(TestCase):
    @patch("auth.views.token_is_valid")
    def setUp(self, token_is_valid):
        token_is_valid.return_value = True
        httpretty.enable()

        self.factory = RequestFactory()
        self.request = self.factory.post('/', data={"key": "value"})
        self.request.session = {'tsuru_token': 'tokentest'}

        url = "{}/docker/node".format(settings.TSURU_HOST)
        httpretty.register_uri(
            httpretty.POST,
            url,
            body="{}",
            status=200
        )
        self.response = NodeAdd.as_view()(self.request)

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    def test_view(self):
        self.assertEqual(self.response.status_code, 200)
