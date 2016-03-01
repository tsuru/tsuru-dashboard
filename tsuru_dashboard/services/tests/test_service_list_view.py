from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory

from tsuru_dashboard import settings
from tsuru_dashboard.services.views import ListService


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

        self.assertIn("services/list.html", response.template_name)
        self.assertEqual(expected, response.context_data['services'])

        url = '{}/services/instances'.format(settings.TSURU_HOST)
        get.assert_called_with(url, headers={'authorization': 'admin'})

    @patch('requests.get')
    def test_empty_list(self, get):
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}

        list_response = Mock(status_code=204)
        list_response.json.side_effect = ValueError

        auth_response = Mock(status_code=200)
        auth_response.json.return_value = []
        response = Mock()
        response.status_code = 204
        response.json.return_value = []

        def do_get(*args, **kwargs):
            if response.status_code == 204:
                response.status_code = 200
                response.json.side_effect = None
            elif response.status_code == 200:
                response.status_code = 204
                response.json.side_effect = ValueError
            return response

        get.side_effect = do_get
        response = ListService.as_view()(request)

        self.assertIn("services/list.html", response.template_name)
        self.assertEqual([], response.context_data['services'])

        url = '{}/services/instances'.format(settings.TSURU_HOST)
        get.assert_called_with(url, headers={'authorization': 'admin'})
