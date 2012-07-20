from django.http import HttpResponseRedirect
from django.test import TestCase
from django.test.client import RequestFactory

from auth.views import Logout


class LogoutViewTest(TestCase):

    def test_should_remove_tsuru_token_from_session(self):
        request = RequestFactory().get('/logout/')
        request.session = {'tsuru_token': 'my beautiful token'}
        Logout().get(request)
        token = request.session.get('tsuru_token')
        self.assertIsNone(token)

    def test_should_redirect_to_index(self):
        request = RequestFactory().get('/logout/')
        request.session = {'tsuru_token': 'my beautiful token'}
        response = Logout().get(request)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual('/', response['Location'])

    def test_should_redirect_to_index_if_the_user_is_not_logged_in(self):
        request = RequestFactory().get('/logout/')
        request.session = {}
        response = Logout().get(request)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual('/', response['Location'])