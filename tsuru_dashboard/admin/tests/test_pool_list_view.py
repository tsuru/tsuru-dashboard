from mock import patch, Mock
from dateutil import parser

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
            "machines": None,
            "nodes": [
                {"Address": "http://128.0.0.1:4243",
                    "Metadata": {"LastSuccess": "2014-08-01T14:09:40-03:00",
                                 "pool": "theonepool"},
                 "Status": "ready"},
                {"Address": "http://127.0.0.1:2375",
                 "Metadata": {"LastSuccess": "2014-08-01T14:09:40-03:00",
                              "pool": "theonepool"},
                 "Status": "ready"},
                {"Address": "http://myserver.com:2375",
                 "Metadata": {"LastSuccess": "2014-08-01T14:09:40-03:00",
                              "pool": "theonepool"},
                 "Status": "ready"},
                {"Address": "https://myserver.com:2376",
                 "Metadata": {"LastSuccess": "2014-08-01T14:09:40-03:00",
                              "pool": "dev\\dev.example.com"},
                 "Status": "ready"},
                {"Address": "https://myserver2.com:2376",
                 "Pool": "dev\\dev.example.com",
                 "Metadata": {"LastSuccess": "2014-08-01T14:09:40-03:00"},
                 "Status": "ready"},
                {"Address": "kubernetes nodes",
                 "Metadata": None,
                 "Status": "ERROR: unable to connect to cluster c1: http://c1.somewhere: connection refused"},
            ],
        }
        body = json.dumps(data)
        httpretty.register_uri(httpretty.GET, url, body=body)

        addrs = ["http://128.0.0.1:4243", "http://myserver.com:2375", "http://127.0.0.1:2375",
                 "https://myserver.com:2376", "https://myserver2.com:2376"]
        hostAddrs = ["128.0.0.1", "myserver.com",
                     "127.0.0.1", "myserver.com", "myserver2.com"]
        for addr, hostAddr in zip(addrs, hostAddrs):
            url = "{}/docker/node/{}/containers".format(
                settings.TSURU_HOST, addr)
            body = json.dumps(
                [{"Status": "started", "HostAddr": hostAddr}, {"Status": "stopped", "HostAddr": hostAddr}])
            httpretty.register_uri(httpretty.GET, url, body=body, status=200)
        url = "{}/docker/node/kubernetes nodes/containers".format(settings.TSURU_HOST)
        httpretty.register_uri(httpretty.GET, url, status=500)

        response = PoolList.as_view()(self.request)

        date = parser.parse("2014-08-01T14:09:40-03:00")
        expected = {
            "None": [
                {"address": "kubernetes nodes",
                 "units_stats": {},
                 "metadata": {},
                 "last_success": None,
                 "pool": "None",
                 "units": [],
                 "status": "ERROR: unable to connect to cluster c1: http://c1.somewhere: connection refused"},
            ],
            "theonepool": [
                {"address": "http://128.0.0.1:4243",
                 "units_stats": {"started": 1, "stopped": 1, "total": 2},
                 "metadata": {"LastSuccess": "2014-08-01T14:09:40-03:00", "pool": "theonepool"},
                 "last_success": date,
                 "pool": "theonepool",
                 "units": [{"HostAddr": "128.0.0.1", "Status": "started"}, {"HostAddr": "128.0.0.1", "Status": "stopped"}],
                 "status": "ready"},
                {"address": "http://127.0.0.1:2375",
                 "units_stats": {"started": 1, "stopped": 1, "total": 2},
                 "metadata": {"LastSuccess": "2014-08-01T14:09:40-03:00", "pool": "theonepool"},
                 "last_success": date,
                 "pool": "theonepool",
                 "units": [{"HostAddr": "127.0.0.1", "Status": "started"}, {"HostAddr": "127.0.0.1", "Status": "stopped"}],
                 "status": "ready"},
                {"address": "http://myserver.com:2375",
                 "units_stats": {"started": 1, "stopped": 1, "total": 2},
                 "metadata": {"LastSuccess": "2014-08-01T14:09:40-03:00", "pool": "theonepool"},
                 "last_success": date,
                 "pool": "theonepool",
                 "units": [{"HostAddr": "myserver.com", "Status": "started"}, {"HostAddr": "myserver.com", "Status": "stopped"}],
                 "status": "ready"},
            ],
            "dev\\dev.example.com": [
                {"address": "https://myserver.com:2376",
                 "units_stats": {"started": 1, "stopped": 1, "total": 2},
                 "metadata": {"LastSuccess": "2014-08-01T14:09:40-03:00", "pool": "dev\\dev.example.com"},
                 "last_success": date,
                 "pool": "dev\\dev.example.com",
                 "units": [{"HostAddr": "myserver.com", "Status": "started"}, {"HostAddr": "myserver.com", "Status": "stopped"}],
                 "status": "ready"},
                {"address": "https://myserver2.com:2376",
                 "units_stats": {"started": 1, "stopped": 1, "total": 2},
                 "metadata": {"LastSuccess": "2014-08-01T14:09:40-03:00"},
                 "last_success": date,
                 "pool": "dev\\dev.example.com",
                 "units": [{"HostAddr": "myserver2.com", "Status": "started"},
                           {"HostAddr": "myserver2.com", "Status": "stopped"}],
                 "status": "ready"},
            ],
        }
        self.assertEqual(sorted(expected.items()),
                         response.context_data["pools"])

    @httpretty.activate
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_without_units_by_node(self, token_is_valid):
        token_is_valid.return_value = True

        url = "{}/docker/node".format(settings.TSURU_HOST)
        data = {
            "machines": None,
            "nodes": [
                {"Address": "http://128.0.0.1:4243",
                    "Metadata": {"LastSuccess": "2014-08-01T14:09:40-03:00",
                                 "pool": "theonepool"},
                 "Status": "ready"},
                {"Address": "http://127.0.0.1:2375",
                 "Metadata": {"LastSuccess": "2014-08-01T14:09:40-03:00",
                              "pool": "theonepool"},
                 "Status": "ready"},
                {"Address": "http://myserver.com:2375",
                 "Metadata": {"LastSuccess": "2014-08-01T14:09:40-03:00",
                              "pool": "theonepool"},
                 "Status": "ready"},
            ],
        }
        body = json.dumps(data)
        httpretty.register_uri(httpretty.GET, url, body=body)

        for addr in ["http://128.0.0.1:4243", "http://myserver.com:2375", "http://127.0.0.1:2375"]:
            url = "{}/docker/node/{}/containers".format(
                settings.TSURU_HOST, addr)
            httpretty.register_uri(httpretty.GET, url, status=403)

        response = PoolList.as_view()(self.request)

        date = parser.parse("2014-08-01T14:09:40-03:00")
        expected = {"theonepool": [
            {"address": "http://128.0.0.1:4243",
             "units_stats": {},
             "units": [],
             "pool": "theonepool",
             "metadata": {"LastSuccess": "2014-08-01T14:09:40-03:00", "pool": "theonepool"},
             "last_success": date,
             "status": "ready"},
            {"address": "http://127.0.0.1:2375",
             "units_stats": {},
             "units": [],
             "pool": "theonepool",
             "metadata": {"LastSuccess": "2014-08-01T14:09:40-03:00", "pool": "theonepool"},
             "last_success": date,
             "status": "ready"},
            {"address": "http://myserver.com:2375",
             "units_stats": {},
             "units": [],
             "pool": "theonepool",
             "metadata": {"LastSuccess": "2014-08-01T14:09:40-03:00", "pool": "theonepool"},
             "last_success": date,
             "status": "ready"},
        ]}
        self.assertEqual(sorted(expected.items()),
                         response.context_data["pools"])
