from dateutil import parser

import mock
import httpretty
import json

from django.test import TestCase
from django.test.client import RequestFactory

from tsuru_dashboard import settings
from tsuru_dashboard.admin.views import PoolInfo


class PoolInfoViewTest(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}

    @httpretty.activate
    @mock.patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_should_use_list_template(self, token_is_valid):
        token_is_valid.return_value = True

        url = "{}/docker/node".format(settings.TSURU_HOST)
        body = json.dumps({})
        httpretty.register_uri(httpretty.GET, url, body=body, status=200)

        response = PoolInfo.as_view()(self.request, pool="mypool")

        self.assertIn("docker/pool_info.html", response.template_name)
        self.assertEqual({}, response.context_data["pools"])

    @httpretty.activate
    @mock.patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_should_pass_addresses_to_the_template(self, token_is_valid):
        token_is_valid.return_value = True

        data = {
            "machines": None,
            "nodes": [
                {"Address": "http://128.0.0.1:4243",
                    "Metadata": {"LastSuccess": "2014-08-01T14:09:40-03:00",
                                 "pool": "mypool"},
                 "Status": "ready"},
                {"Address": "http://127.0.0.1:2375",
                 "Metadata": {"LastSuccess": "2014-08-01T14:09:40-03:00",
                              "pool": "mypool"},
                 "Status": "ready"},
                {"Address": "http://myserver.com:2375",
                 "Metadata": {"LastSuccess": "2014-08-01T14:09:40-03:00",
                              "pool": "theonepool"},
                 "Status": "ready"},
            ],
        }

        url = "{}/docker/node".format(settings.TSURU_HOST)
        body = json.dumps(data)
        httpretty.register_uri(httpretty.GET, url, body=body, status=200)

        for addr in ["http://128.0.0.1:4243", "http://myserver.com:2375", "http://127.0.0.1:2375"]:
            url = "{}/docker/node/{}/containers".format(settings.TSURU_HOST, addr)
            body = json.dumps(
                [{"Status": "started", "HostAddr": addr}, {"Status": "stopped", "HostAddr": addr}])
            httpretty.register_uri(httpretty.GET, url, body=body, status=200)

        response = PoolInfo.as_view()(self.request, pool="mypool")
        date = parser.parse("2014-08-01T14:09:40-03:00")
        expected = {"mypool": [
            {"Address": "http://128.0.0.1:4243",
             "Units": {"started": 1, "stopped": 1, "total": 2},
             "Metadata": {"LastSuccess": date, "pool": "mypool"},
             "Status": "ready"},
            {"Address": "http://127.0.0.1:2375",
             "Units": {"started": 1, "stopped": 1, "total": 2},
             "Metadata": {"LastSuccess": date, "pool": "mypool"},
             "Status": "ready"},
        ]}
        self.assertEqual(expected, response.context_data["pools"])

    @httpretty.activate
    @mock.patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_without_units_by_node(self, token_is_valid):
        token_is_valid.return_value = True

        data = {
            "machines": None,
            "nodes": [
                {"Address": "http://128.0.0.1:4243",
                    "Metadata": {"LastSuccess": "2014-08-01T14:09:40-03:00",
                                 "pool": "mypool"},
                 "Status": "ready"},
                {"Address": "http://127.0.0.1:2375",
                 "Metadata": {"LastSuccess": "2014-08-01T14:09:40-03:00",
                              "pool": "mypool"},
                 "Status": "ready"},
                {"Address": "http://myserver.com:2375",
                 "Metadata": {"LastSuccess": "2014-08-01T14:09:40-03:00",
                              "pool": "theonepool"},
                 "Status": "ready"},
            ],
        }

        url = "{}/docker/node".format(settings.TSURU_HOST)
        body = json.dumps(data)
        httpretty.register_uri(httpretty.GET, url, body=body, status=200)

        for addr in ["http://128.0.0.1:4243", "http://myserver.com:2375", "http://127.0.0.1:2375"]:
            url = "{}/docker/node/{}/containers".format(settings.TSURU_HOST, addr)
            body = json.dumps([{"Status": "started"}, {"Status": "stopped"}])
            httpretty.register_uri(httpretty.GET, url, body=body, status=403)

        response = PoolInfo.as_view()(self.request, pool="mypool")
        date = parser.parse("2014-08-01T14:09:40-03:00")
        expected = {"mypool": [
            {"Address": "http://128.0.0.1:4243",
             "Units": {},
             "Metadata": {"LastSuccess": date, "pool": "mypool"},
             "Status": "ready"},
            {"Address": "http://127.0.0.1:2375",
             "Units": {},
             "Metadata": {"LastSuccess": date, "pool": "mypool"},
             "Status": "ready"},
        ]}
        self.assertEqual(expected, response.context_data["pools"])
