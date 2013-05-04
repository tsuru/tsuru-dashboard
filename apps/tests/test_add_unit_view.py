from mock import patch

from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory

from apps.views import UnitAdd


class UnitAddViewTest(TestCase):
    @patch('requests.put')
    def test_should_use_list_template(self, put):
        data = {"units": '4'}
        request = RequestFactory().post("/", data)
        request.session = {"tsuru_token": "admin"}
        response = UnitAdd.as_view()(request, app_name="app_name")
        self.assertEqual(200, response.status_code)
        put.assert_called_with(
            '{0}/apps/app_name/units'.format(settings.TSURU_HOST),
            data='4',
            headers={'authorization': 'admin'}
        )
