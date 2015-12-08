from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory

from tsuru_dashboard import settings
from tsuru_dashboard.teams.views import List


class ListTeamViewTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}

    @patch('requests.get')
    def test_should_use_list_template(self, get):
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = []
        get.return_value = response_mock

        response = List.as_view()(self.request)

        self.assertIn("teams/list.html", response.template_name)
        expected = []
        self.assertListEqual(expected, response.context_data['teams'])
        get.assert_called_with(
            '{}/teams'.format(settings.TSURU_HOST),
            headers={'authorization': 'admin'})

    @patch('requests.get')
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_should_return_empty_list_when_status_is_204(self, token_is_valid, get):
        token_is_valid.return_value = True
        get.return_value = Mock(status_code=204)

        response = List.as_view()(self.request)

        self.assertIn("teams/list.html", response.template_name)
        expected = []
        self.assertListEqual(expected, response.context_data['teams'])
        get.assert_called_with(
            '{}/teams'.format(settings.TSURU_HOST),
            headers={'authorization': 'admin'})
