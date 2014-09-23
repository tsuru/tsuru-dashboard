from mock import patch, Mock

from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory

from admin.views import ListNode


class ListNodeViewTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}

    @patch("requests.get")
    def test_should_use_list_template(self, get):
        response_mock = Mock()
        response_mock.json.return_value = {}
        get.return_value = response_mock
        response = ListNode.as_view()(self.request)
        self.assertEqual("docker/list_node.html", response.template_name)
        expected = []
        self.assertListEqual(expected, response.context_data["nodes"])
        get.assert_called_with(
            "{0}/docker/node".format(settings.TSURU_HOST),
            headers={"authorization": "admin"})

    @patch("requests.get")
    def test_should_pass_addresses_to_the_template(self, get):
        response_mock = Mock()
        response_mock.json.return_value = {
            "machines": None,
            "nodes": [
                {"Address": "http://128.0.0.1:4243",
                 "Metadata": {"LastSuccess": "2014-08-01T14:09:40Z",
                              "pool": "theonepool"},
                 "Status": "ready"},
                {"Address": "http://127.0.0.1:2375",
                 "Metadata": {"LastSuccess": "2014-08-01T14:09:40Z",
                              "pool": "theonepool"},
                 "Status": "ready"},
                {"Address": "http://myserver.com:2375",
                 "Metadata": {"LastSuccess": "2014-08-01T14:09:40Z",
                              "pool": "theonepool"},
                 "Status": "ready"},
            ],
        }
        get.return_value = response_mock
        response = ListNode.as_view()(self.request)
        expected = [
            {"Address": "http://128.0.0.1:4243",
             "Metadata": {"LastSuccess": "2014-08-01T14:09:40Z",
                          "pool": "theonepool"},
             "Status": "ready"},
            {"Address": "http://127.0.0.1:2375",
             "Metadata": {"LastSuccess": "2014-08-01T14:09:40Z",
                          "pool": "theonepool"},
             "Status": "ready"},
            {"Address": "http://myserver.com:2375",
             "Metadata": {"LastSuccess": "2014-08-01T14:09:40Z",
                          "pool": "theonepool"},
             "Status": "ready"},
        ]
        self.assertListEqual(expected, response.context_data["nodes"])
