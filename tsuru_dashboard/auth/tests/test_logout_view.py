from django.http import HttpResponseRedirect
from django.test import TestCase
from django.test.client import RequestFactory

from tsuru_dashboard.auth.views import Logout


class TestLogoutWhenUserIsLoggedIn(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/logout/')
        self.request.session = {'tsuru_token': 'my beautiful token'}
        self.response = Logout.as_view()(self.request)

    def test_should_remove_tsuru_token_from_session(self):
        token = self.request.session.get('tsuru_token')
        self.assertIsNone(token)

    def test_should_redirect_to_index(self):
        self.assertIsInstance(self.response, HttpResponseRedirect)
        self.assertEqual('/', self.response['Location'])


class TestLogoutWhenUserIsLogout(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/logout/')
        self.request.session = {}
        self.response = Logout.as_view()(self.request)

    def test_should_redirect_to_index(self):
        self.assertIsInstance(self.response, HttpResponseRedirect)
        self.assertEqual('/', self.response['Location'])
