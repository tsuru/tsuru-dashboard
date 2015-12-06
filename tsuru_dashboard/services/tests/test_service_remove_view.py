from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory
from django.conf import settings
from django.core.urlresolvers import reverse

from tsuru_dashboard.services.views import ServiceRemove


class ServiceRemoveViewTest(TestCase):
    @patch("requests.delete")
    @patch("requests.get")
    def test_view(self, get, delete):
        get.return_value = Mock(status_code=200)
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}
        service_name = "service"
        response = ServiceRemove.as_view()(request, instance=service_name)
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse("service-list"), response.items()[1][1])
        delete.assert_called_with(
            '{0}/services/instances/{1}'.format(
                settings.TSURU_HOST,
                service_name),
            headers={'authorization': 'admin'})
