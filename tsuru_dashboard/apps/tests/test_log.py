from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory

from tsuru_dashboard.apps.views import LogStream


class LogTest(TestCase):
    @patch("requests.get")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_log(self, token_is_valid, get):
        def stream():
            yield "message"

        iter_lines = Mock()
        iter_lines.return_value = stream

        token_is_valid.return_value = True
        get.iter_lines.return_value = iter_lines

        self.request = RequestFactory().get("/apps/app-teste/log/")
        self.request.session = {'tsuru_token': 'tokentest'}
        self.app_name = 'app-teste'

        LogStream.as_view()(self.request, app_name=self.app_name)
