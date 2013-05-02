from django.http import HttpResponse, HttpResponseRedirect
from django.test import TestCase
from django.test.client import RequestFactory

from auth.views import LoginRequiredView


class LoginRequiredViewTest(TestCase):

    def test_should_redirect_to_login_page_if_user_is_not_authenticated(self):
        request = RequestFactory().get('/')
        request.session = {}
        response = StubView.as_view()(request)
        self.assertIsInstance(response, HttpResponseRedirect)
        expected_url = '/'
        self.assertEqual(expected_url, response['Location'])

    def test_should_invoke_view_dispatch_when_user_is_authenticated(self):
        request = RequestFactory().get('/')
        request.session = {'tsuru_token': 'my beautiful token'}
        response = StubView.as_view()(request)
        self.assertEqual('ok', response.content)


class StubView(LoginRequiredView):

    def get(self, request):
        return HttpResponse('ok')
