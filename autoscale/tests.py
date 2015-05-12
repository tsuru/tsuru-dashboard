from django.test import TestCase
from django.core.urlresolvers import reverse


class IndexTestCase(TestCase):
    def test_index(self):
        response = self.client.get(reverse("autoscale"))
        self.assertTemplateUsed(response, "autoscale/index.html")
