from django.test import TestCase
from django.test.client import RequestFactory
from django.conf import settings
from django.core.urlresolvers import reverse

from auth.views import ChangePassword
from auth.forms import ChangePasswordForm

import json

from mock import patch, Mock


class TestResetPasswordView(TestCase):
    def test_get(self):
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "ble"}
        response = ChangePassword.as_view()(request)
        self.assertIn('auth/change_password.html',
                      response.template_name)
        self.assertIsInstance(response.context_data['form'],
                              ChangePasswordForm)

    @patch("django.contrib.messages.error")
    @patch("requests.put")
    def test_post(self, put, error):
        data = {
            "old": "old",
            "new": "new",
            "confirm": "new",
        }
        request = RequestFactory().post("/", data)
        request.session = {'tsuru_token': 'tokentest'}
        response = ChangePassword.as_view()(request)
        headers = {'authorization': 'tokentest'}
        url = "{0}/users/password".format(settings.TSURU_HOST)
        put.assert_called_with(url, data=json.dumps(data), headers=headers)
        self.assertEqual(302, response.status_code)
        self.assertEqual('/auth/change-password/', response.items()[1][1])

    @patch("django.contrib.messages.success")
    @patch("requests.put")
    def test_post_sends_success_message(self, put, success):
        put.return_value = Mock(status_code=200)
        data = {
            "old": "old",
            "new": "new",
            "confirm": "new",
        }
        request = RequestFactory().post("/", data)
        request.session = {'tsuru_token': 'tokentest'}
        ChangePassword.as_view()(request)
        success.assert_called_with(request, u'Password successfully updated!', fail_silently=True)

    @patch("django.contrib.messages.error")
    @patch("requests.put")
    def test_post_sends_error_message(self, put, error):
        put.return_value = Mock(status_code=403, text=u'error')
        data = {
            "old": "old",
            "new": "new",
            "confirm": "new",
        }
        request = RequestFactory().post("/", data)
        request.session = {'tsuru_token': 'tokentest'}
        ChangePassword.as_view()(request)
        error.assert_called_with(request, u'error', fail_silently=True)

    def test_login_required(self):
        request = RequestFactory().get("/")
        request.session = {}
        response = ChangePassword.as_view()(request)
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse('login'), response.items()[1][1])
