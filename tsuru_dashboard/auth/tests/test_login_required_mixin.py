from django.http import HttpResponse, HttpResponseRedirect
from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.views.generic.base import View

from tsuru_dashboard import settings
from tsuru_dashboard.auth.views import LoginRequiredMixin

from mock import patch, Mock


class LoginRequiredMixinTest(TestCase):

    @patch("requests.get")
    def test_should_redirect_to_login_page_if_user_is_not_authenticated(self, get):
        get.return_value = Mock(status_code=200)
        request = RequestFactory().get('/')
        request.session = {}
        response = StubView.as_view()(request)
        self.assertIsInstance(response, HttpResponseRedirect)
        expected_url = "%s?next=%s" % (reverse('login'), request.path)
        self.assertEqual(expected_url, response['Location'])

    @patch("requests.get")
    def test_should_invoke_view_dispatch_when_user_is_authenticated(self, get):
        get.return_value = Mock(status_code=200)
        request = RequestFactory().get('/')
        request.session = {'tsuru_token': 'my beautiful token'}
        response = StubView.as_view()(request)
        self.assertEqual('ok', response.content)

    def test_authorization(self):
        view = StubView()

        request = RequestFactory().get('/')
        request.session = {'tsuru_token': 'my beautiful token'}

        view.request = request
        headers = view.authorization

        expected = {'authorization': 'my beautiful token'}
        self.assertDictEqual(headers, expected)

    def test_client(self):
        view = StubView()

        request = RequestFactory().get('/')
        request.session = {'tsuru_token': 'type mytoken'}

        view.request = request
        client = view.client

        self.assertEqual(client.templates.target, settings.TSURU_HOST)
        self.assertEqual(client.templates.token, "mytoken")


class StubView(LoginRequiredMixin, View):

    def get(self, request):
        return HttpResponse('ok')
