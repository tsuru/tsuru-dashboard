from django.test import TestCase
from django.core.urlresolvers import reverse

from auth.forms import PasswordRecoveryForm


class PasswordRecoveryViewTest(TestCase):
    def test_get(self):
        response = self.client.get(reverse('password-recovery'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('auth/password_recovery.html')
        self.assertIsInstance(response.context['form'], PasswordRecoveryForm)
