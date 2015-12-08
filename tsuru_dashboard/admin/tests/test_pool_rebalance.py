from mock import patch

from django.test import TestCase
from django.test.client import RequestFactory

import httpretty

from tsuru_dashboard import settings
from tsuru_dashboard.admin.views import PoolRebalance


class PoolRebalanceTest(TestCase):
    def setUp(self):
        httpretty.enable()

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_view(self, token_is_valid):
        token_is_valid.return_value = True

        factory = RequestFactory()
        request = factory.post('/')
        request.session = {'tsuru_token': 'tokentest'}

        url = "{}/docker/containers/rebalance".format(settings.TSURU_HOST)
        httpretty.register_uri(
            httpretty.POST,
            url,
            body="{}",
            status=200
        )

        response = PoolRebalance.as_view()(request, pool="mypool")

        self.assertEqual(response.status_code, 200)
