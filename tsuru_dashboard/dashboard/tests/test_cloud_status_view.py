from django.test import TestCase
from django.test import client

from tsuru_dashboard import settings
from tsuru_dashboard.auth.views import LoginRequiredView
from tsuru_dashboard.dashboard import views

import mock
import json
import httpretty


class CloudStatusTest(TestCase):

    def setUp(self):
        self.request = client.RequestFactory().get("/")
        self.request.session = {"tsuru_token": "sometoken"}

    def test_requires_login(self):
        assert issubclass(views.CloudStatusView, LoginRequiredView), \
            "CloudStatusView should inherit from LoginRequiredView"

    @httpretty.activate
    @mock.patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_without_access(self, token_is_valid):
        token_is_valid.return_value = True

        url = "{}/docker/node".format(settings.TSURU_HOST)
        httpretty.register_uri(httpretty.GET, url, status=403)

        url = "{}/apps".format(settings.TSURU_HOST)
        httpretty.register_uri(httpretty.GET, url, status=403)

        response = views.CloudStatusView.as_view()(self.request)
        data = json.loads(response.content)

        self.assertEqual(0, data["total_nodes"])
        self.assertEqual(0, data["total_apps"])
        self.assertEqual(0, data["total_containers"])
        self.assertEqual(0, data["containers_by_nodes"])

    @httpretty.activate
    @mock.patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_total_nodes(self, token_is_valid):
        token_is_valid.return_value = True

        url = "{}/apps".format(settings.TSURU_HOST)
        httpretty.register_uri(httpretty.GET, url, status=403)

        url = "{}/docker/node".format(settings.TSURU_HOST)
        body = json.dumps({"nodes": [1, 2, 3, 4]})
        httpretty.register_uri(httpretty.GET, url, body=body, status=200)

        response = views.CloudStatusView.as_view()(self.request)
        data = json.loads(response.content)

        self.assertEqual(4, data["total_nodes"])

    @httpretty.activate
    @mock.patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_total_apps_and_containers(self, token_is_valid):
        token_is_valid.return_value = True

        url = "{}/apps".format(settings.TSURU_HOST)
        body = json.dumps([{"units": [1, 2, 3]}])
        httpretty.register_uri(httpretty.GET, url, body=body, status=200)

        url = "{}/docker/node".format(settings.TSURU_HOST)
        httpretty.register_uri(httpretty.GET, url, body=body, status=403)

        response = views.CloudStatusView.as_view()(self.request)
        data = json.loads(response.content)

        self.assertEqual(1, data["total_apps"])
        self.assertEqual(3, data["total_containers"])

    @httpretty.activate
    @mock.patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_containers_by_node(self, token_is_valid):
        token_is_valid.return_value = True

        url = "{}/apps".format(settings.TSURU_HOST)
        body = json.dumps([{"units": [1, 2, 3, 4, 5, 6]}])
        httpretty.register_uri(httpretty.GET, url, body=body, status=200)

        url = "{}/docker/node".format(settings.TSURU_HOST)
        body = json.dumps({"nodes": [1, 2]})
        httpretty.register_uri(httpretty.GET, url, body=body, status=200)

        response = views.CloudStatusView.as_view()(self.request)
        data = json.loads(response.content)

        self.assertEqual(3, data["containers_by_nodes"])
