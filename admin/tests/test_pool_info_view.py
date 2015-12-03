from mock import patch, Mock
from dateutil import parser

import httpretty

from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory

from admin.views import PoolInfo


class PoolInfoViewTest(TestCase):
    def setUp(self):
        httpretty.enable()
        self.maxDiff = None
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    @patch("requests.get")
    @patch("auth.views.token_is_valid")
    def test_should_use_list_template(self, token_is_valid, get):
        token_is_valid.return_value = True
        response_mock = Mock()
        response_mock.json.return_value = {}
        get.return_value = response_mock
        response = PoolInfo.as_view()(self.request, pool="mypool")
        self.assertIn("docker/pool_info.html", response.template_name)
        expected = {}
        self.assertEqual(expected, response.context_data["pools"])
        get.assert_called_with(
            "{0}/docker/node".format(settings.TSURU_HOST),
            headers={"authorization": "admin"})

    @patch("requests.get")
    @patch("auth.views.token_is_valid")
    def test_should_pass_addresses_to_the_template(self, token_is_valid, get):
        token_is_valid.return_value = True
        response_mock = Mock()
        response_mock.json.return_value = {
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
                {"Address": "http://myserver2.com:2375",
                 "Metadata": {"LastSuccess": "2014-08-01T14:09:40-03:00"},
                 "Status": "ready"},
            ],
        }
        get.return_value = response_mock
        PoolInfo.units_by_node = Mock()
        PoolInfo.units_by_node.return_value = {"started": 1, "stopped": 2}

        response = PoolInfo.as_view()(self.request, pool="mypool")
        date = parser.parse("2014-08-01T14:09:40-03:00")
        expected = {"mypool": [
            {"Address": "http://128.0.0.1:4243",
             "Units": {"started": 1, "stopped": 2},
             "Metadata": {"LastSuccess": date, "pool": "mypool"},
             "Status": "ready"},
            {"Address": "http://127.0.0.1:2375",
             "Units": {"started": 1, "stopped": 2},
             "Metadata": {"LastSuccess": date, "pool": "mypool"},
             "Status": "ready"},
        ]}
        self.assertEqual(expected, response.context_data["pools"])
