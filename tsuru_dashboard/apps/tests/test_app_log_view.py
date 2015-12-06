from mock import patch

from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from tsuru_dashboard.apps.views import AppLog


class AppLogViewTest(TestCase):
    @patch("requests.get")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def setUp(self, token_is_valid, get):
        token_is_valid.return_value = True
        self.request = RequestFactory().get("/apps/app-teste/log/")
        self.request.session = {'tsuru_token': 'tokentest'}
        self.app_name = 'app-teste'
        self.response = AppLog.as_view()(self.request, app_name=self.app_name)

    def test_run_should_render_expected_template(self):
        self.assertIn('apps/app_log.html', self.response.template_name)

    def test_context_should_contain_app(self):
        self.assertIn('app', self.response.context_data)

    def test_get_request_run_url_should_not_return_404(self):
        response = self.client.get(reverse('app_log', args=[self.app_name]))
        self.assertNotEqual(404, response.status_code)
