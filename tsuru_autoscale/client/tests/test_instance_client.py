import httpretty
from django.test import TestCase

from tsuru_autoscale import settings
from tsuru_autoscale.client.instance import InstanceClient


class InstanceClientTestCase(TestCase):
    def setUp(self):
        self.target = "http://autoscalehost.com"
        self.token = "token"
        self.client = InstanceClient(self.target, self.token)
        httpretty.enable()

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    def test_list(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://autoscalehost.com/service/instance",
        )

        self.client.list()

    def test_get(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://autoscalehost.com/service/instance/name",
        )

        self.client.get("name")

    def test_alarms_by_instance(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://autoscalehost.com/alarm/instance/name",
        )

        self.client.alarms_by_instance("name")
