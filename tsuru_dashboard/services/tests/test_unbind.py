from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from tsuru_dashboard import settings
from tsuru_dashboard.services.views import Unbind

from mock import patch, Mock


class UnbindViewTest(TestCase):
    @patch("requests.delete")
    @patch("requests.get")
    def test_view(self, get, delete):
        get.return_value = Mock(status_code=200)
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}
        instance = "instance"
        app = "app"
        service = "service"

        response = Unbind.as_view()(request, service=service, instance=instance, app=app)

        self.assertEqual(302, response.status_code)
        url = reverse('service-detail', args=[service, instance])
        self.assertEqual(url, response.items()[1][1])
        url = '{}/services/{}/instances/{}/{}'.format(settings.TSURU_HOST, service, instance, app)
        delete.assert_called_with(url, headers={'authorization': 'admin'})
