from django.test import TestCase
from django.test.client import RequestFactory
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from tsuru_dashboard.apps.views import RemoveApp

import mock


class RemoveAppTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/name/remove")
        self.request.session = {"tsuru_token": "admin"}

    @mock.patch('requests.delete')
    @mock.patch('requests.get')
    def test_should_returns_404_when_app_does_not_exists(self, get, delete):
        get.return_value = mock.Mock(status_code=200)
        delete.return_value = mock.Mock(status_code=404, text="app not found")
        response = RemoveApp.as_view()(self.request, name="appname")
        self.assertEqual(404, response.status_code)
        self.assertEqual("app not found", response.content)

    @mock.patch('requests.delete')
    @mock.patch('requests.get')
    def test_should_redirect_to_the_app_list(self, get, delete):
        get.return_value = mock.Mock(status_code=200)
        delete.return_value = mock.Mock(status_code=200)
        response = RemoveApp.as_view()(self.request, name="appname")
        self.assertEqual(302, response.status_code)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(reverse('list-app'), response['Location'])
