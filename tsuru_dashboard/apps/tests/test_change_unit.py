from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory

from tsuru_dashboard import settings
from tsuru_dashboard.apps.views import ChangeUnit


class ChangeUnitViewTest(TestCase):
    @patch('requests.get')
    @patch('requests.delete')
    def test_remove_unit(self, delete, get):
        data = {
            "name": "app1",
            "units": [
                {"Ip": "10.10.10.10"},
                {"Ip": "9.9.9.9"},
                {"Ip": "8.8.8.8"},
                {"Ip": "7.7.7.7"}
            ],
        }
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = data
        get.return_value = response_mock

        data = {"units": '1'}
        request = RequestFactory().post("/", data)
        request.session = {"tsuru_token": "admin"}

        ChangeUnit.as_view()(request, app_name="app_name")

        delete.assert_called_with(
            '{}/apps/app_name/units'.format(settings.TSURU_HOST),
            data='3',
            headers={'authorization': 'admin'}
        )

        get.assert_called_with(
            '{}/apps/app_name'.format(settings.TSURU_HOST),
            headers={'authorization': 'admin'}
        )

    @patch('requests.get')
    @patch('requests.put')
    def test_add_unit(self, put, get):
        data = {
            "name": "app1",
            "units": [
                {"Ip": "10.10.10.10"},
                {"Ip": "9.9.9.9"},
            ],
        }
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = data
        get.return_value = response_mock

        data = {"units": '10'}
        request = RequestFactory().post("/", data)
        request.session = {"tsuru_token": "admin"}

        ChangeUnit.as_view()(request, app_name="app_name")

        put.assert_called_with(
            '{}/apps/app_name/units'.format(settings.TSURU_HOST),
            data='8',
            headers={'authorization': 'admin'}
        )

        get.assert_called_with(
            '{}/apps/app_name'.format(settings.TSURU_HOST),
            headers={'authorization': 'admin'}
        )

    @patch('requests.get')
    def test_redirect_to_the_app_detail_page(self, get):
        data = {
            "name": "app1",
            "units": [
                {"Ip": "10.10.10.10"},
                {"Ip": "9.9.9.9"},
            ],
        }
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = data
        get.return_value = response_mock

        data = {"units": '2'}
        request = RequestFactory().post("/", data)
        request.session = {"tsuru_token": "admin"}

        response = ChangeUnit.as_view()(request, app_name="app_name")

        self.assertEqual(302, response.status_code)
        self.assertEqual("/apps/app_name/", response.items()[1][1])

        get.assert_called_with(
            '{}/apps/app_name'.format(settings.TSURU_HOST),
            headers={'authorization': 'admin'}
        )
