from mock import patch

from django.test import TestCase
from django.test.client import RequestFactory
from django.conf import settings

from services.views import ServiceAdd


class ServiceAddViewTest(TestCase):
    @patch("requests.post")
    def test_post(self, post):
        data = {"name": "name"}
        request = RequestFactory().post("/", data)
        request.session = {"tsuru_token": "admin"}
        response = ServiceAdd.as_view()(request, service_name="service")
        self.assertEqual(302, response.status_code)
        post.assert_called_with(
            '{0}/services/instances'.format(settings.TSURU_HOST),
            headers={'authorization': 'admin'},
            data={"name": "name"})

    def test_get(self):
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}
        response = ServiceAdd.as_view()(request, service_name="service")
        self.assertEqual(200, response.status_code)
