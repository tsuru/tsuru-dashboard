from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.conf import settings

from apps.views import AutoscaleEnable

from mock import patch


class AutoscaleEnableTest(TestCase):

    def test_method_not_allowed(self):
        methods = ["get", "put", "delete"]
        for method in methods:
            request = getattr(RequestFactory(), method)("/")
            request.session = {"tsuru_token": "admin"}
            response = AutoscaleEnable.as_view()(request, app_name="app1")
            self.assertEqual(response.status_code, 405)

    @patch("requests.put")
    def test_enabled(self, put_mock):
        app_name = "app1"

        request = RequestFactory().post("/")
        request.session = {"tsuru_token": "admin"}

        response = AutoscaleEnable.as_view()(request, app_name=app_name)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], reverse('detail-app', args=[app_name]))

        url = "{}/autoscale/{}/enable".format(settings.TSURU_HOST, app_name)
        headers = {'authorization': request.session["tsuru_token"]}
        put_mock.assert_called_with(url, headers=headers)
