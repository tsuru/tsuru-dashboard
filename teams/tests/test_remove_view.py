from mock import patch

from django.test import TestCase
from django.test.client import RequestFactory
from django.conf import settings
from django.core.urlresolvers import reverse

from teams.views import Remove


class RemoveViewTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}

    @patch("requests.delete")
    def test_view(self, delete):
        team_name = "avengers"
        response = Remove.as_view()(self.request, team=team_name)
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse("team-list"), response.items()[1][1])
        delete.assert_called_with(
            '{0}/teams/{1}'.format(
                settings.TSURU_HOST,
                team_name),
            headers={'authorization': 'admin'})
