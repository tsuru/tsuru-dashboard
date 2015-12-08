from mock import patch

from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

import httpretty
import json

from tsuru_dashboard import settings
from tsuru_dashboard.admin.views import NodeInfo


class NodeInfoViewTest(TestCase):
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def setUp(self, token_is_valid):
        token_is_valid.return_value = True
        httpretty.enable()

        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.session = {'tsuru_token': 'tokentest'}

        self.address = 'http://127.0.0.2:4243'

        url = "{}/docker/node/{}/containers".format(settings.TSURU_HOST, '127.0.0.2')
        self.containers = [
            {"id": "blabla", "type": "python", "appname": "myapp", "hostaddr": "http://127.0.0.2:4243"}
        ]
        httpretty.register_uri(
            httpretty.GET,
            url,
            body=json.dumps(self.containers),
            status=200
        )

        url = "{}/docker/node".format(settings.TSURU_HOST, self.address)
        self.nodes = {
            "nodes": [
                {
                    "Status": "ready",
                    "Metadata": {
                        "pool": "tsuru1",
                        "iaas": "ec2",
                        "LastSuccess": "2015-11-16T18:44:36-02:00",
                    },
                    "Address": "http://127.0.0.2:4243"
                },
                {
                    "Status": "ready",
                    "Metadata": {
                        "pool": "tsuru2",
                        "iaas": "ec2",
                        "LastSuccess": "2015-11-16T18:44:36-02:00",
                    },
                    "Address": "http://127.0.0.3:4243"
                },
            ]
        }
        httpretty.register_uri(
            httpretty.GET,
            url,
            body=json.dumps(self.nodes),
            status=200
        )
        self.response = NodeInfo.as_view()(self.request, address=self.address)

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    def test_should_use_list_template(self):
        self.assertIn("admin/node_info.html", self.response.template_name)

    def teste_should_get_list_of_containers_from_tsuru(self):
        self.assertListEqual(self.containers, self.response.context_data["containers"])

    def teste_should_get_node_info_from_tsuru(self):
        self.assertDictEqual(self.nodes["nodes"][0], self.response.context_data["node"])

    def test_get_request_run_url_should_not_return_404(self):
        response = self.client.get(reverse('node-info', args=[self.address.replace("http://", "")]))
        self.assertNotEqual(404, response.status_code)

    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def teste_should_get_list_of_containers_empty_list(self, token_is_valid):
        httpretty.reset()
        token_is_valid.return_value = True

        url = "{}/docker/node/{}/containers".format(settings.TSURU_HOST, '127.0.0.2')
        httpretty.register_uri(
            httpretty.GET,
            url,
            status=204
        )

        url = "{}/docker/node".format(settings.TSURU_HOST, self.address)
        httpretty.register_uri(
            httpretty.GET,
            url,
            body=json.dumps(self.nodes),
            status=200
        )
        response = NodeInfo.as_view()(self.request, address=self.address)
        self.assertListEqual([], response.context_data["containers"])

    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def teste_should_get_list_of_containers_on_error(self, token_is_valid):
        httpretty.reset()
        token_is_valid.return_value = True

        url = "{}/docker/node/{}/containers".format(settings.TSURU_HOST, '127.0.0.2')
        httpretty.register_uri(
            httpretty.GET,
            url,
            status=500
        )

        url = "{}/docker/node".format(settings.TSURU_HOST, self.address)
        httpretty.register_uri(
            httpretty.GET,
            url,
            body=json.dumps(self.nodes),
            status=200
        )
        response = NodeInfo.as_view()(self.request, address=self.address)
        self.assertListEqual([], response.context_data["containers"])

    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def teste_should_get_empty_node(self, token_is_valid):
        httpretty.reset()
        token_is_valid.return_value = True

        url = "{}/docker/node/{}/containers".format(settings.TSURU_HOST, '127.0.0.2')
        httpretty.register_uri(
            httpretty.GET,
            url,
            body=json.dumps(self.containers),
            status=200
        )

        url = "{}/docker/node".format(settings.TSURU_HOST, self.address)
        httpretty.register_uri(
            httpretty.GET,
            url,
            status=204
        )
        response = NodeInfo.as_view()(self.request, address=self.address)
        self.assertFalse(response.context_data["node"])
