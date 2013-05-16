from django.test import TestCase
from django.core.urlresolvers import reverse


class TokeRequestSuccessViewTest(TestCase):
    def test_get(self):
        response = self.client.get(reverse('token-request-success'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('auth/token_request_success.html')
