from mock import patch

from django.test import TestCase
from django.test.client import RequestFactory
from django.conf import settings
from django.core.urlresolvers import reverse

from apps.views import AppRevokeTeam


class AppRevokeTeamTestCase(TestCase):

    @patch("requests.delete")
    def test_view(self, delete):
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}
        app_name = "app_name"
        team = "team"
        response = AppRevokeTeam.as_view()(request,
                                           app_name=app_name,
                                           team=team)
        self.assertEqual(302, response.status_code)
        url = reverse('app-teams', args=[app_name])
        self.assertEqual(url, response.items()[1][1])
        delete.assert_called_with(
            "{0}/apps/{1}/{2}".format(
                settings.TSURU_HOST,
                app_name, team
            ),
            headers={'authorization': 'admin'})
