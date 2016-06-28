from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from tsuru_dashboard.auth.views import LoginRequiredMixin, KeysList


class KeysListViewTest(TestCase):
    @patch("requests.get")
    def setUp(self, get):
        get.return_value = Mock(status_code=200)
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.session = {"tsuru_token": "admin"}
        self.response = KeysList.as_view()(self.request)

    def test_should_require_login_to_create_team(self):
        assert issubclass(KeysList, LoginRequiredMixin)

    def test_key_should_render_expected_template(self):
        self.assertIn('auth/key_list.html', self.response.template_name)

    def test_get_request_key_url_should_not_return_404(self):
        response = self.client.get(reverse('list-keys'))
        self.assertNotEqual(404, response.status_code)
