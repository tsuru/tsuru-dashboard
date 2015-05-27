from mock import patch

from django.test import TestCase
from django.test.client import RequestFactory
from django.conf import settings
from django.core.urlresolvers import reverse

from services.views import ServiceAdd

import json


class ServiceAddViewTest(TestCase):
    @patch("requests.post")
    def test_post(self, post):
        data = {"name": "name", "team": "team"}
        request = RequestFactory().post("/", data)
        request.session = {"tsuru_token": "admin"}
        response = ServiceAdd.as_view()(request, service_name="service")
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse('service-list'), response.items()[1][1])
        post.assert_called_with(
            '{0}/services/instances'.format(settings.TSURU_HOST),
            headers={'authorization': 'admin'},
            data=json.dumps({"name": "name", "team": "team", "service_name": "service"}))

    @patch("requests.get")
    def test_get(self, get):
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}
        response = ServiceAdd.as_view()(request, service_name="service")
        self.assertEqual(200, response.status_code)
