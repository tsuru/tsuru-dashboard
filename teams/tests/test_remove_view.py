from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory
from django.conf import settings
from django.core.urlresolvers import reverse

from teams.views import Remove


class RemoveViewTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}

    @patch("django.contrib.messages.error")
    @patch("requests.delete")
    def test_view(self, delete, error):
        team_name = "avengers"
        response = Remove.as_view()(self.request, team=team_name)
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse("team-list"), response.items()[1][1])
        delete.assert_called_with(
            '{0}/teams/{1}'.format(
                settings.TSURU_HOST,
                team_name),
            headers={'authorization': 'admin'})

    @patch("django.contrib.messages.error")
    @patch("requests.delete")
    def test_view_should_send_error_message(self, delete, error):
        delete.return_value = Mock(status_code=403,
                                   text=u'Can not delete this team!')
        team_name = "avengers"
        Remove.as_view()(self.request, team=team_name)
        error.assert_called_with(self.request, u'Can not delete this team!', fail_silently=True)
