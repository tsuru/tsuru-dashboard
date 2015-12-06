from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory
from django.conf import settings
from django.core.urlresolvers import reverse

from tsuru_dashboard.services.views import Bind


class BindViewTest(TestCase):
    @patch("requests.put")
    @patch("requests.get")
    def test_view(self, get, put):
        get.return_value = Mock(status_code=200)
        app = "app"
        request = RequestFactory().post("/", {"app": app})
        request.session = {"tsuru_token": "admin"}
        instance = "service"
        response = Bind.as_view()(request,
                                  instance=instance)
        self.assertEqual(302, response.status_code)
        url = reverse('service-detail', args=[instance])
        self.assertEqual(url, response.items()[1][1])
        put.assert_called_with(
            '{0}/services/instances/{1}/{2}'.format(
                settings.TSURU_HOST,
                instance,
                app
            ),
            headers={'authorization': 'admin'})
