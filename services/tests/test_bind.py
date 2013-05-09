from mock import patch

from django.test import TestCase
from django.test.client import RequestFactory
from django.conf import settings
from django.core.urlresolvers import reverse

from services.views import Bind


class BindViewTest(TestCase):
    @patch("requests.put")
    def test_view(self, put):
        request = RequestFactory().post("/")
        request.session = {"tsuru_token": "admin"}
        instance = "service"
        app_name = "app"
        response = Bind.as_view()(request,
                                  instance=instance,
                                  app_name=app_name)
        self.assertEqual(302, response.status_code)
        url = reverse('service-detail', args=[instance])
        self.assertEqual(url, response.items()[1][1])
        put.assert_called_with(
            '{0}/services/instances/{1}/{2}'.format(
                settings.TSURU_HOST,
                instance,
                app_name
            ),
            headers={'authorization': 'admin'})
