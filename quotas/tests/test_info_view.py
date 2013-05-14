from django.test import TestCase
from django.test.client import RequestFactory
from django.conf import settings

from quotas.views import Info

from mock import patch, Mock


class InfoViewTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin",
                                "username": "raul@seixas.com"}

    @patch("requests.get")
    def test_view(self, get):
        data = {
            'available': 2,
            'items': ["tank/1", "tank/2"]
        }
        response_mock = Mock()
        response_mock.json.return_value = data
        get.return_value = response_mock
        response = Info.as_view()(self.request)
        self.assertEqual("quota/info.html", response.template_name)
        get.assert_called_with(
            '{0}/quota/{1}'.format(settings.TSURU_HOST,
                                   self.request.session["username"]),
            headers={'authorization': 'admin'}
        )
        self.assertEqual(data['available'], response.context_data['available'])
        self.assertListEqual(data['items'], response.context_data['items'])
