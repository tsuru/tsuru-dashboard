from django.test import TestCase
from django.test.client import RequestFactory

from teams.views import Info


class InfoViewTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}

    def test_view(self):
        response = Info.as_view()(self.request, name="avengers")
        self.assertEqual("teams/info.html", response.template_name)
