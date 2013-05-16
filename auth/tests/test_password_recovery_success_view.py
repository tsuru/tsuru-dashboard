from django.test import TestCase
from django.core.urlresolvers import reverse


class PasswordRecoverySuccessViewTest(TestCase):
    def test_get(self):
        response = self.client.get(reverse('password-recovery-success'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('auth/password_recovery_success.html')
