from django.test import TestCase
from django.test.client import RequestFactory
from django.http import HttpResponseRedirect

from apps.views import RemoveApp

import mock

class RemoveAppTestCase(TestCase):
    def test_should_returns_404_when_app_does_not_exists(self):
        request = RequestFactory().get("/name/remove")
        request.session = {"tsuru_token":"admin"}
        with mock.patch('requests.delete') as delete:
            delete.return_value = mock.Mock(status_code=404, text="app not found")
            response = RemoveApp.as_view()(request, name="appname")
        self.assertEqual(404, response.status_code)
        self.assertEqual("app not found", response.content)

    def test_should_redirect_to_the_app_list(self):
        request = RequestFactory().get("/name/remove")
        request.session = {"tsuru_token":"admin"}
        with mock.patch('requests.delete') as delete:
            delete.return_value = mock.Mock(status_code=200)
            response = RemoveApp.as_view()(request, name="appname")
        self.assertEqual(302, response.status_code)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual("/app", response.items()[1][1])
