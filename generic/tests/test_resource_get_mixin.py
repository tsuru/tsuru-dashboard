from django.test import TestCase
from django.test.client import RequestFactory

from generic.resources import ResouceGetMixin


class ResouceGetMixinTest(TestCase):
    def setUp(self):
        request = RequestFactory().get("/")
        request.session = {'tsuru_token': 'ble'}
        self.mixin = ResouceGetMixin()
        self.mixin.request = request

    def test_get_headers(self):
        expected = {
            'authorization': 'ble'
        }
        headers = self.mixin.get_headers()
        self.assertDictEqual(expected, headers)
