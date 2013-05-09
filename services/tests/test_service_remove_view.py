from mock import patch

from django.test import TestCase
from django.test.client import RequestFactory
from django.conf import settings
from django.core.urlresolvers import reverse

from services.views import ServiceRemove


class ServiceRemoveViewTest(TestCase):
    @patch("requests.delete")
    def test_view(self, delete):
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
