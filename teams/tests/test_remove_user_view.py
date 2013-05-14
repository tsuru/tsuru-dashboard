from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.conf import settings

from teams.views import RemoveUser

from mock import patch


class RemoveUserViewTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}

    @patch("requests.delete")
    def test_view(self, delete):
        team_name = "avengers"
        user = "username"
        response = RemoveUser.as_view()(self.request, team=team_name,
                                        user=user)
        self.assertEqual(302, response.status_code)
        url = reverse("team-info", args=[team_name])
        self.assertEqual(url, response.items()[1][1])
        url = "{0}/teams/{1}/{2}".format(settings.TSURU_HOST, team_name, user)
        headers = {"authorization": "admin"}
        delete.assert_called_with(url, headers=headers)
