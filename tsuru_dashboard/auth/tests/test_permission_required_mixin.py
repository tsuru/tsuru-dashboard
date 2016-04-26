from django.http import HttpResponse, HttpResponseRedirect
from django.test import TestCase
from django.test.client import RequestFactory
from django.views.generic.base import View

from tsuru_dashboard.auth.views import PermissionRequiredMixin

from mock import patch, Mock


class PermissionRequiredMixinTest(TestCase):

    @patch("requests.get")
    def test_should_redirect_user_when_user_doesnt_have_permission(self, get):
        get.return_value = Mock(status_code=200)
        request = RequestFactory().get('/')
        request.session = {'permissions': {"super": False}}
        response = StubView.as_view()(request)
        self.assertIsInstance(response, HttpResponseRedirect)
        expected_url = "/"
        self.assertEqual(expected_url, response['Location'])

    @patch("requests.get")
    def test_should_invoke_view_dispatch_when_user_has_permission(self, get):
        get.return_value = Mock(status_code=200)
        request = RequestFactory().get('/')
        request.session = {'permissions': {"super": True}}
        response = StubView.as_view()(request)
        self.assertEqual('ok', response.content)


class StubView(PermissionRequiredMixin, View):

    required_permission = "super"

    def get(self, request):
        return HttpResponse('ok')
