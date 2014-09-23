from django.test import TestCase
from django.core.urlresolvers import reverse


class HealthcheckTest(TestCase):
    def test_view(self):
        response = self.client.get(reverse("healthcheck"))
        self.assertEqual(200, response.status_code)
        self.assertEqual("WORKING", response.content)
