from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory

from tsuru_dashboard.auth.views import LoginRequiredView
from tsuru_dashboard.apps.views import AppRollback


class AppRollbackViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/")
        self.request.session = {"tsuru_token": "admin"}

    def test_should_require_login_to_rollback_app(self):
        assert issubclass(AppRollback, LoginRequiredView)

    @patch("requests.post")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_post_with_valid_app_and_image(self, token_is_valid, post):
        token_is_valid.return_value = True
        m = Mock(status_code=200, content="")
        post.return_value = m
        response = AppRollback.as_view()(
            self.request, app_name='test', image='localhost:3030/tsuru/app-test:v44')
        self.assertEqual(200, response.status_code)
