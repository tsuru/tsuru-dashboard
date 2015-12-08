from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from tsuru_dashboard import settings
from tsuru_dashboard.teams.views import Remove

import mock


class RemoveViewTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}

    @mock.patch("django.contrib.messages.error")
    @mock.patch("requests.delete")
    @mock.patch("requests.get")
    def test_view(self, get, delete, error):
        get.return_value = mock.Mock(status_code=200)
        team_name = "avengers"
        response = Remove.as_view()(self.request, team=team_name)
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse("team-list"), response.items()[1][1])
        delete.assert_called_with(
            '{0}/teams/{1}'.format(
                settings.TSURU_HOST,
                team_name),
            headers={'authorization': 'admin'})

    @mock.patch("django.contrib.messages.error")
    @mock.patch("requests.delete")
    @mock.patch("requests.get")
    def test_view_should_send_error_message(self, get, delete, error):
        get.return_value = mock.Mock(status_code=200)
        delete.return_value = mock.Mock(status_code=403, text=u'Can not delete this team!')
        team_name = "avengers"
        Remove.as_view()(self.request, team=team_name)
        error.assert_called_with(self.request, u'Can not delete this team!', fail_silently=True)
