from django.test import TestCase
from django.core.urlresolvers import reverse

import mock
import requests


class HealthcheckTest(TestCase):

    @mock.patch("requests.get")
    def test_healthcheck_ok(self, get_mock):
        get_mock.return_value = mock.Mock(status_code=200, text="WORKING")

        response = self.client.get(reverse("healthcheck"))

        self.assertEqual(200, response.status_code)
        self.assertEqual("WORKING", response.content)

    @mock.patch("requests.get")
    def test_healthcheck_connection_error(self, get_mock):
        get_mock.side_effect = requests.exceptions.ConnectionError()

        response = self.client.get(reverse("healthcheck"))

        self.assertEqual(500, response.status_code)
        self.assertEqual("Failed to connect to tsuru.", response.content)

    @mock.patch("requests.get")
    def test_healthcheck_wrong_status_code(self, get_mock):
        get_mock.return_value = mock.Mock(status_code=500, text="WORKING")

        response = self.client.get(reverse("healthcheck"))

        self.assertEqual(500, response.status_code)
        self.assertEqual("Failed to connect to tsuru.", response.content)

    @mock.patch("requests.get")
    def test_healthcheck_wrong_text(self, get_mock):
        get_mock.return_value = mock.Mock(status_code=200, text="not expected")

        response = self.client.get(reverse("healthcheck"))

        self.assertEqual(500, response.status_code)
        self.assertEqual("Failed to connect to tsuru.", response.content)
