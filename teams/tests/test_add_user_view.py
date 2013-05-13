from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from teams.views import AddUser


class AddUserViewTest(TestCase):
    def setUp(self):
        data = {"user": "username"}
        self.request = RequestFactory().post("/", data)
        self.request.session = {"tsuru_token": "admin"}

    def test_view(self):
        team_name = "avengers"
        response = AddUser.as_view()(self.request, team=team_name)
        self.assertEqual(302, response.status_code)
        url = reverse("team-info", args=[team_name])
        self.assertEqual(url, response.items()[1][1])
