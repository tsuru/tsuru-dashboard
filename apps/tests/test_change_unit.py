from mock import patch

from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory

from apps.views import ChangeUnit

from pluct.resource import Resource
from pluct.schema import Schema


class ChangeUnitViewTest(TestCase):
    @patch('pluct.resource.get')
    @patch('requests.delete')
    def test_remove_unit(self, delete, get):
        schema = Schema(
            "",
            type="object",
            properties={
                "units":
                {
                    "type": "array",
                    "items": {},
                }
            }
        )
        resource_data = {
            "name": "app1",
            "units": [
                {"Ip": "10.10.10.10"},
                {"Ip": "9.9.9.9"},
                {"Ip": "8.8.8.8"},
                {"Ip": "7.7.7.7"}
            ],
        }
        resource = Resource(
            url="url.com",
            data=resource_data,
            schema=schema,
        )
        get.return_value = resource
        data = {"units": '1'}
        request = RequestFactory().post("/", data)
        request.session = {"tsuru_token": "admin"}
        ChangeUnit.as_view()(request, app_name="app_name")
        delete.assert_called_with(
            '{0}/apps/app_name/units'.format(settings.TSURU_HOST),
            data='3',
            headers={'authorization': 'admin'}
        )

    @patch('pluct.resource.get')
    @patch('requests.put')
    def test_add_unit(self, put, get):
        resource_data = {
            "name": "app1",
            "units": [
                {"Ip": "10.10.10.10"},
                {"Ip": "9.9.9.9"},
            ],
        }
        schema = Schema(
            "",
            type="object",
            properties={
                "units":
                {
                    "type": "array",
                    "items": {},
                }
            }
        )
        resource = Resource(
            url="url.com",
            data=resource_data,
            schema=schema
        )
        get.return_value = resource
        data = {"units": '10'}
        request = RequestFactory().post("/", data)
        request.session = {"tsuru_token": "admin"}
        ChangeUnit.as_view()(request, app_name="app_name")
        put.assert_called_with(
            '{0}/apps/app_name/units'.format(settings.TSURU_HOST),
            data='8',
            headers={'authorization': 'admin'}
        )

    @patch('pluct.resource.get')
    def test_redirect_to_the_app_detail_page(self, get):
        resource_data = {
            "name": "app1",
            "units": [
                {"Ip": "10.10.10.10"},
                {"Ip": "9.9.9.9"},
            ],
        }
        schema = Schema(
            "",
            type="object",
            properties={
                "units":
                {
                    "type": "array",
                    "items": {},
                }
            }
        )
        resource = Resource(
            url="url.com",
            data=resource_data,
            schema=schema
        )
        get.return_value = resource
        data = {"units": '2'}
        request = RequestFactory().post("/", data)
        request.session = {"tsuru_token": "admin"}
        response = ChangeUnit.as_view()(request, app_name="app_name")
        self.assertEqual(302, response.status_code)
        self.assertEqual("/apps/app_name/", response.items()[1][1])
