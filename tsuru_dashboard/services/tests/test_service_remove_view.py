from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from tsuru_dashboard import settings
from tsuru_dashboard.services.views import ServiceRemove


class ServiceRemoveViewTest(TestCase):
    @patch("requests.delete")
    @patch("requests.get")
    def test_view(self, get, delete):
        get.return_value = Mock(status_code=200)
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}
        instance = "instance"
        service = "service"

        response = ServiceRemove.as_view()(request, service=service, instance=instance)

        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse("service-list"), response.items()[1][1])
        url = '{}/services/{}/instances/{}'.format(settings.TSURU_HOST, service, instance)
        delete.assert_called_with(url, headers={'authorization': 'admin'})
