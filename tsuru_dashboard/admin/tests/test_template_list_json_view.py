from mock import patch

from django.test import TestCase
from django.test.client import RequestFactory

import httpretty
import json

from tsuru_dashboard import settings
from tsuru_dashboard.admin.views import TemplateListJson


class TemplateListJsonTest(TestCase):
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def setUp(self, token_is_valid):
        token_is_valid.return_value = True
        httpretty.enable()

        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.session = {'tsuru_token': 'tokentest'}

        url = "{}/iaas/templates".format(settings.TSURU_HOST)
        self.templates = []
        httpretty.register_uri(
            httpretty.GET,
            url,
            body=json.dumps(self.templates),
            status=200
        )
        self.response = TemplateListJson.as_view()(self.request)

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    def teste_view(self):
        data = json.loads(self.response.content)
        self.assertListEqual(self.templates, data)
