from mock import patch

from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory

from apps.views import UnitRemove


class UnitRemoveViewTest(TestCase):
    @patch('requests.delete')
    def test_view(self, delete):
        data = {"units": '4'}
        request = RequestFactory().post("/", data)
        request.session = {"tsuru_token": "admin"}
        response = UnitRemove.as_view()(request, app_name="app_name")
        self.assertEqual(200, response.status_code)
        delete.assert_called_with(
            '{0}/apps/app_name/units'.format(settings.TSURU_HOST),
            data='4',
            headers={'authorization': 'admin'}
        )
