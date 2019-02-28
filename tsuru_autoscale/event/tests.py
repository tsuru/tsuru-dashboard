from django.test import TestCase
from django.core.urlresolvers import reverse

from tsuru_autoscale.event import client

import httpretty
import mock

import os


class ListTestCase(TestCase):
    @mock.patch("tsuru_autoscale.event.client.list")
    def test_list(self, list_mock):
        url = "{}?TSURU_TOKEN=bla".format(reverse("event-list", args=["alarm_name"]))
        response = self.client.get(url)

        self.assertTemplateUsed(response, "event/list.html")
        self.assertIn('list', response.context)
        list_mock.assert_called_with("alarm_name", "bla")


class ClientTestCase(TestCase):
    def setUp(self):
        httpretty.enable()

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    def test_list(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.GET,
            "http://autoscalehost.com/alarm/abc/event",
        )

        client.list("abc", "token")
