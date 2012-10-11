from django.test import TestCase
from django.test.client import RequestFactory

from apps.views import RemoveApp

import mock

class RemoveAppTestCase(TestCase):
    def test_should_returns_404_when_app_does_not_exists(self):
        request = RequestFactory().get("/name/remove")
        request.session = {"tsuru_token":"admin"}
        with mock.patch('requests.delete') as delete:
            delete.return_value = mock.Mock(status_code=404, text="app not found")
            response = RemoveApp.as_view()(request, name="appname")
        self.assertEqual(404, response.status_code)
        self.assertEqual("app not found", response.content)
