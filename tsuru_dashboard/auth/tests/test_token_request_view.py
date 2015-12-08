from django.test import TestCase
from django.core.urlresolvers import reverse

from tsuru_dashboard import settings
from tsuru_dashboard.auth.forms import TokenRequestForm

from mock import patch, Mock


class TokeRequestViewTest(TestCase):
    def test_get(self):
        response = self.client.get(reverse('token-request'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('auth/token_request.html')
        self.assertIsInstance(response.context['form'], TokenRequestForm)

    @patch("requests.post")
    @patch("requests.get")
    def test_send_when_form_is_valid(self, get, post):
        get.return_value = Mock(status_code=200)
        response = self.client.post(reverse('token-request'),
                                    {"email": "some@email.com"})
        self.assertRedirects(response, reverse('token-request-success'))
        url = "{0}/users/{1}/password".format(settings.TSURU_HOST,
                                              "some@email.com")
        post.assert_called_with(url)
