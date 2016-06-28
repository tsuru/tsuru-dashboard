import json

from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from tsuru_dashboard import settings
from tsuru_dashboard.auth.views import KeysRemove


class KeysRemoveViewTest(TestCase):
    @patch("requests.delete")
    @patch("requests.get")
    def test_view(self, get, delete):
        get.return_value = Mock(status_code=200)
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}
        key = "rsa"

        response = KeysRemove.as_view()(request, key=key)
        payload = {'name': key}

        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse("list-keys"), response.items()[1][1])
        url = '{}/users/keys'.format(settings.TSURU_HOST)
        delete.assert_called_with(url, data=json.dumps(payload), headers={'authorization': 'admin'})
