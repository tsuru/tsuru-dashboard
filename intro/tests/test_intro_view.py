from django.test import TestCase
from django.core.urlresolvers import reverse


class TestIntroView(TestCase):
    def test_get(self):
        response = self.client.get(reverse('intro'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('intro/intro.html')
