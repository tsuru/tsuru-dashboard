from django.test import TestCase
from django.test.client import RequestFactory

from tsuru_dashboard import settings
from tsuru_dashboard.teams.views import Info

from mock import patch, Mock


class InfoViewTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}
        self.data = {u'name': u'anvenger', u'users': [u'ironman', u'thor']}

    @patch("requests.get")
    def test_view(self, get):
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = self.data
        get.return_value = response_mock

        response = Info.as_view()(self.request, team="avengers")

        self.assertIn("teams/info.html", response.template_name)
        self.assertDictEqual(self.data, response.context_data['team'])
        get.assert_called_with(
            '{0}/teams/{1}'.format(settings.TSURU_HOST, "avengers"),
            headers={'authorization': 'admin'}
        )
