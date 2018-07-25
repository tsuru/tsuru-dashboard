from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory

from tsuru_dashboard import settings
from tsuru_dashboard.admin.views import PoolList

import json
import httpretty


class PoolListViewTest(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}

    @patch("requests.get")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_should_use_list_template(self, token_is_valid, get):
        token_is_valid.return_value = True

        response_mock = Mock()
        response_mock.json.return_value = {}
        get.return_value = response_mock

        response = PoolList.as_view()(self.request)

        self.assertIn("admin/pool_list.html", response.template_name)
        self.assertEqual([], response.context_data["pools"])
        url = "{}/docker/node".format(settings.TSURU_HOST)
        get.assert_called_with(url, headers={"authorization": "admin"})

    @httpretty.activate
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_should_pass_addresses_to_the_template(self, token_is_valid):
        token_is_valid.return_value = True

        url = "{}/docker/node".format(settings.TSURU_HOST)
        data = {
            "nodes": [
                {"Address": "http://128.0.0.1:4243",
                 "Status": "ready",
                 "Pool": "theonepool"},
                {"Address": "http://127.0.0.1:2375",
                 "Status": "ready",
                 "Pool": "theonepool"},
                {"Address": "http://myserver.com:2375",
                 "Status": "ready",
                 "Pool": "theonepool"},
                {"Address": "https://myserver.com:2376",
                 "Status": "ready",
                 "Pool": "dev\\dev.example.com"},
                {"Address": "https://myserver2.com:2376",
                 "Status": "ready",
                 "Pool": "dev\\dev.example.com"},
                {"Address": "kubernetes nodes",
                 "Status": "ERROR: unable to connect to cluster c1: http://c1.somewhere: connection refused",
                 "Pool": "kube"},
            ],
        }
        body = json.dumps(data)
        httpretty.register_uri(httpretty.GET, url, body=body)
        response = PoolList.as_view()(self.request)

        expected = {
            "kube": json.dumps([
                {"address": "kubernetes nodes",
                 "status": "ERROR: unable to connect to cluster c1: http://c1.somewhere: connection refused"},
            ]),
            "theonepool": json.dumps([
                {"address": "http://128.0.0.1:4243",
                 "status": "ready"},
                {"address": "http://127.0.0.1:2375",
                 "status": "ready"},
                {"address": "http://myserver.com:2375",
                 "status": "ready"},
            ]),
            "dev\\dev.example.com": json.dumps([
                {"address": "https://myserver.com:2376",
                 "status": "ready"},
                {"address": "https://myserver2.com:2376",
                 "status": "ready"},
            ]),
        }
        self.assertEqual(sorted(expected.items()),
                         response.context_data["pools"])

    @httpretty.activate
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_should_map_nodes_without_pool(self, token_is_valid):
        token_is_valid.return_value = True

        url = "{}/docker/node".format(settings.TSURU_HOST)
        data = {
            "nodes": [
                {"Address": "http://128.0.0.1:4243",
                 "Status": "ready",
                 "Pool": "theonepool"},
                {"Address": "http://127.0.0.1:2375",
                 "Status": "ready",
                 "Pool": ""},
                {"Address": "http://myserver.com:2375",
                 "Status": "ready",
                 "Pool": ""},
            ],
        }
        body = json.dumps(data)
        httpretty.register_uri(httpretty.GET, url, body=body)
        response = PoolList.as_view()(self.request)

        expected = {
            "theonepool": json.dumps([
                {"address": "http://128.0.0.1:4243",
                 "status": "ready"},
            ]),
            "": json.dumps([
                {"address": "http://127.0.0.1:2375",
                 "status": "ready"},
                {"address": "http://myserver.com:2375",
                 "status": "ready"},
            ]),
        }
        self.assertEqual(sorted(expected.items()),
                         response.context_data["pools"])
