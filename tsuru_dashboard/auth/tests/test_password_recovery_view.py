from django.test import TestCase
from django.core.urlresolvers import reverse

from tsuru_dashboard import settings
from tsuru_dashboard.auth.forms import PasswordRecoveryForm

from mock import patch, Mock


class PasswordRecoveryViewTest(TestCase):
    def test_get(self):
        response = self.client.get(reverse('password-recovery'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('auth/password_recovery.html')
        self.assertIsInstance(response.context['form'], PasswordRecoveryForm)

    @patch("requests.post")
    @patch("requests.get")
    def test_send_when_form_is_valid(self, get, post):
        get.return_value = Mock(status_code=200)
        response = self.client.post(reverse('password-recovery'),
                                    {"email": "some@email.com", "token": "tt"})
        self.assertRedirects(response, reverse('password-recovery-success'))
        url = "{0}/users/{1}/password?token={2}".format(
            settings.TSURU_HOST,
            "some@email.com",
            "tt"
        )
        post.assert_called_with(url)
