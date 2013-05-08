from django.test import TestCase
from django.test.client import RequestFactory

from services.views import ServiceInstanceDetail


class ServiceInstanceDetailViewTest(TestCase):
    def test_view(self):
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}
        response = ServiceInstanceDetail.as_view()(request,
                                                   service_name="service")
        self.assertEqual("services/detail.html", response.template_name)
        self.assertDictEqual({"name": "service"},
                             response.context_data['service'])
