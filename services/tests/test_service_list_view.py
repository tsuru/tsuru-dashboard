from mock import patch, Mock

from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory

from services.views import ListService


class ListServiceViewTest(TestCase):
    @patch('requests.get')
    def test_should_use_list_template(self, get):
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}
        expected = {"teste": "teste"}

        response_mock = Mock(status_code=200)
        response_mock.json.return_value = expected
        get.return_value = response_mock

        response = ListService.as_view()(request)

        self.assertEqual("services/list.html", response.template_name)
        self.assertDictEqual(expected, response.context_data['services'])

        url = '{}/services/instances'.format(settings.TSURU_HOST)
        get.assert_called_with(url, headers={'authorization': 'admin'})
