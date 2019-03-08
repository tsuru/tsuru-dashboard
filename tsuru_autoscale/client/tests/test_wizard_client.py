import json
import httpretty
from django.test import TestCase

from tsuru_autoscale import settings
from tsuru_autoscale.client.wizard import WizardClient

class WizardClientTestCase(TestCase):
    def setUp(self):
        self.target = "http://autoscalehost.com"
        self.token = "token"
        self.client = WizardClient(self.target, self.token)
        httpretty.enable()

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    def test_new(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://autoscalehost.com/wizard",
        )

        self.client.new({})

    def test_get(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://autoscalehost.com/wizard/name",
        )

        self.client.get("name")

    def test_events(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://autoscalehost.com/wizard/name/events",
        )

        self.client.events("name")

    def test_remove(self):
        httpretty.register_uri(
            httpretty.DELETE,
            "http://autoscalehost.com/wizard/name",
        )

        self.client.remove("name")