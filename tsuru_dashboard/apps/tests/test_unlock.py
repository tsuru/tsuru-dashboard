from django.test import TestCase
from django.test.client import RequestFactory
from django.http import HttpResponse
from tsuru_dashboard import settings

from tsuru_dashboard.apps.views import Unlock

import mock


class UnlockTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().post("/name/unlock")
        self.request.session = {"tsuru_token": "admin"}

    @mock.patch('requests.delete')
    @mock.patch('requests.get')
    @mock.patch("django.contrib.messages.error")
    def test_should_returns_404_when_app_does_not_exists(self, msg_mock, get, delete):
        get.return_value = mock.Mock(status_code=200)
        delete.return_value = mock.Mock(status_code=404, text="app not found")

        response = Unlock.as_view()(self.request, name="appname")

        self.assertEqual(404, response.status_code)
        msg_mock.assert_called_with(self.request, 'app not found', fail_silently=True)

    @mock.patch('requests.delete')
    @mock.patch('requests.get')
    @mock.patch("django.contrib.messages.success")
    def test_should_redirect_to_the_settings(self, msg_mock, get, delete):
        get.return_value = mock.Mock(status_code=200)
        delete.return_value = mock.Mock(status_code=200)

        response = Unlock.as_view()(self.request, name="appname")

        self.assertEqual(200, response.status_code)
        self.assertIsInstance(response, HttpResponse)

        url = "{}/apps/appname/lock".format(settings.TSURU_HOST)
        delete.assert_called_with(url, headers={'authorization': 'admin'})
        msg_mock.assert_called_with(self.request, u'App was successfully unlocked', fail_silently=True)
