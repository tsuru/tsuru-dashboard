from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from tsuru_dashboard import settings
from tsuru_dashboard.teams.views import AddUser

from mock import patch, Mock


class AddUserViewTest(TestCase):
    def setUp(self):
        data = {"user": "username"}
        self.request = RequestFactory().post("/", data)
        self.request.session = {"tsuru_token": "admin"}

    @patch("django.contrib.messages.error")
    @patch("requests.put")
    @patch("requests.get")
    def test_view(self, get, put, error):
        get.return_value = Mock(status_code=200)
        team_name = "avengers"
        response = AddUser.as_view()(self.request, team=team_name)
        self.assertEqual(302, response.status_code)
        url = reverse("team-info", args=[team_name])
        self.assertEqual(url, response.items()[1][1])
        url = "{0}/teams/{1}/{2}".format(settings.TSURU_HOST, team_name,
                                         "username")
        headers = {"authorization": "admin"}
        put.assert_called_with(url, headers=headers)
