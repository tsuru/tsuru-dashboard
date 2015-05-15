from django.test import TestCase
from django.core.urlresolvers import reverse


class IndexTestCase(TestCase):
    def test_index(self):
        session = self.client.session
        session['tsuru_token'] = "beare token"
        session.save()

        response = self.client.get(reverse("autoscale"))
        self.assertTemplateUsed(response, "autoscale/index.html")
