from mock import patch

from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory

from services.views import ServiceDetail


class ServiceDetailViewTest(TestCase):
    def test_should_use_list_template(self):
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}
        response = ServiceDetail.as_view()(request, service_name="service")
        self.assertEqual("services/detail.html", response.template_name)
        self.assertDictEqual({"name": "service"},
                             response.context_data['service'])
