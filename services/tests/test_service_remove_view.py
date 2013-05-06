from mock import patch

from django.test import TestCase
from django.test.client import RequestFactory
from django.conf import settings

from services.views import ServiceRemove


class ServiceRemoveViewTest(TestCase):
    @patch("requests.delete")
    def test_view(self, delete):
        request = RequestFactory().post("/")
        request.session = {"tsuru_token": "admin"}
        service_name = "service"
        response = ServiceRemove.as_view()(request, service_name=service_name)
        self.assertEqual(302, response.status_code)
        delete.assert_called_with(
            '{0}/services/c/instances/{1}'.format(
                settings.TSURU_HOST,
                service_name),
            headers={'authorization': 'admin'})
