from django.test import TestCase
from django.test.client import RequestFactory
from django.conf import settings

from auth.views import ChangePassword
from auth.forms import ChangePasswordForm

import json

from mock import patch, Mock


class TestResetPasswordView(TestCase):
    def test_get(self):
        request = RequestFactory().get("/")
        response = ChangePassword.as_view()(request)
        self.assertIn('auth/change_password.html',
                      response.template_name)
        self.assertIsInstance(response.context_data['form'],
                              ChangePasswordForm)

    @patch("requests.put")
    def test_post(self, put):
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
    def test_post_sends_sucess_message(self, put, success):
        put.return_value = Mock(status_code=200)
        data = {
            "old": "old",
            "new": "new",
            "confirm": "new",
        }
        request = RequestFactory().post("/", data)
        request.session = {'tsuru_token': 'tokentest'}
        ChangePassword.as_view()(request)
        success.assert_called_with(request, u'Password successfully updated!')
