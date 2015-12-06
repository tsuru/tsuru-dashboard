from django.test import TestCase
from django.test.client import RequestFactory
from django.conf import settings
from django.core.urlresolvers import reverse

from tsuru_dashboard.services.views import Unbind

from mock import patch, Mock


class UnbindViewTest(TestCase):
    @patch("requests.delete")
    @patch("requests.get")
    def test_view(self, get, delete):
        get.return_value = Mock(status_code=200)
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}
        instance = "instance"
        app = "app"
        response = Unbind.as_view()(request,
                                    instance=instance,
                                    app=app)
        self.assertEqual(302, response.status_code)
        url = reverse('service-detail', args=[instance])
        self.assertEqual(url, response.items()[1][1])
        delete.assert_called_with(
            '{0}/services/instances/{1}/{2}'.format(
                settings.TSURU_HOST,
                instance, app
            ),
            headers={'authorization': 'admin'})
