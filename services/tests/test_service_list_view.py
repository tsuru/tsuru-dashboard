from mock import patch

from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory

from services.views import ListService

from pluct.resource import Resource


class ListServiceViewTest(TestCase):
    @patch('pluct.resource.get')
    def test_should_use_list_template(self, get):
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}
        expected = {"teste": "teste"}
        resource = Resource(url="url", data=expected)
        get.return_value = resource
        response = ListService.as_view()(request)
        self.assertEqual("services/list.html", response.template_name)
        self.assertDictEqual(expected, response.context_data['services'])
        get.assert_called_with(
            '{0}/services'.format(settings.TSURU_HOST),
            {'credentials': 'admin', 'type': 'type'})
