from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from tsuru_dashboard import settings
from tsuru_dashboard.teams.views import RemoveUser

from mock import patch, Mock


class RemoveUserViewTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}

    @patch("django.contrib.messages.error")
    @patch("requests.delete")
    @patch("requests.get")
    def test_view(self, get, delete, error):
        get.return_value = Mock(status_code=200)
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

    @patch("django.contrib.messages.success")
    @patch("requests.delete")
    @patch("requests.get")
    def test_view_should_send_success_message(self, get, delete, success):
        get.return_value = Mock(status_code=200)
        delete.return_value = Mock(status_code=200)
        team_name = "avengers"
        user = "username"
        RemoveUser.as_view()(self.request, team=team_name,
                             user=user)
        success.assert_called_with(self.request, u'User successfully removed!', fail_silently=True)

    @patch("django.contrib.messages.error")
    @patch("requests.delete")
    @patch("requests.get")
    def test_view_should_send_error_message(self, get, delete, error):
        get.return_value = Mock(status_code=200)
        delete.return_value = Mock(status_code=403, text=u'error')
        team_name = "avengers"
        user = "username"
        RemoveUser.as_view()(self.request, team=team_name,
                             user=user)
        error.assert_called_with(self.request, u'error', fail_silently=True)
