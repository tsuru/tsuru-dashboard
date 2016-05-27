from mock import patch

from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

import httpretty
import json

from tsuru_dashboard import settings
from tsuru_dashboard.admin.views import NodeInfoJson


class NodeInfoViewTest(TestCase):
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def setUp(self, token_is_valid):
        token_is_valid.return_value = True
        httpretty.enable()

        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.session = {'tsuru_token': 'tokentest'}

        self.address = 'http://127.0.0.2:4243'

        url = "{}/docker/node/{}/containers".format(settings.TSURU_HOST, 'http://127.0.0.2:4243')
        self.containers = [
            {"id": "blabla", "type": "python", "AppName": "myapp", "hostaddr": "http://127.0.0.2:4243"}
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
        self.response = NodeInfoJson.as_view()(self.request, address=self.address)
        self.responseContent = json.loads(self.response.content)

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    def teste_should_get_list_of_containers_from_tsuru(self):
        containers = self.containers
        containers[0]["DashboardURL"] = u"/apps/myapp/"
        self.assertListEqual(containers, self.responseContent["node"]["containers"])

    def teste_should_get_node_info_from_tsuru(self):
        self.assertDictEqual(self.nodes["nodes"][0], self.responseContent["node"]["info"])

    def test_get_request_run_url_should_not_return_404(self):
        response = self.client.get(reverse('node-info-json', args=[self.address.replace("http://", "")]))
        self.assertNotEqual(404, response.status_code)

    def test_should_return_remove_node_url(self):
        expected = u"/admin/node/http://127.0.0.2:4243/remove/"
        self.assertEqual(expected, self.responseContent["node"]["nodeRemovalURL"])

    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def teste_should_get_list_of_containers_empty_list(self, token_is_valid):
        httpretty.reset()
        token_is_valid.return_value = True

        url = "{}/docker/node/{}/containers".format(settings.TSURU_HOST, 'http://127.0.0.2:4243')
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
        response = NodeInfoJson.as_view()(self.request, address=self.address)
        self.assertListEqual([], json.loads(response.content)["node"]["containers"])

    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def teste_should_get_list_of_containers_on_error(self, token_is_valid):
        httpretty.reset()
        token_is_valid.return_value = True

        url = "{}/docker/node/{}/containers".format(settings.TSURU_HOST, 'http://127.0.0.2:4243')
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
        response = NodeInfoJson.as_view()(self.request, address=self.address)
        self.assertListEqual([], json.loads(response.content)["node"]["containers"])

    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def teste_should_get_empty_node(self, token_is_valid):
        httpretty.reset()
        token_is_valid.return_value = True

        url = "{}/docker/node/{}/containers".format(settings.TSURU_HOST, 'http://127.0.0.2:4243')
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
        response = NodeInfoJson.as_view()(self.request, address=self.address)
        self.assertFalse(json.loads(response.content)["node"]["info"])
