from mock import patch, Mock

from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory

from teams.views import List


class ListServiceViewTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}

    @patch('requests.get')
    def test_should_use_list_template(self, get):
        response_mock = Mock()
        response_mock.json.return_value = []
        get.return_value = response_mock
        response = List.as_view()(self.request)
        self.assertEqual("teams/list.html", response.template_name)
        expected = []
        self.assertListEqual(expected, response.context_data['teams'])
        get.assert_called_with(
            '{0}/teams'.format(settings.TSURU_HOST),
            headers={'authorization': 'admin'})

    @patch('requests.get')
    def test_should_return_empty_list_when_status_is_204(self, get):
        get.return_value = Mock(status_code=204)
        response = List.as_view()(self.request)
        self.assertEqual("teams/list.html", response.template_name)
        expected = []
        self.assertListEqual(expected, response.context_data['teams'])
        get.assert_called_with(
            '{0}/teams'.format(settings.TSURU_HOST),
            headers={'authorization': 'admin'})
