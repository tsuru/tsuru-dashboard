from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory

from auth.views import LoginRequiredView
from apps.views import AppRollback


class AppRollbackViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/")
        self.request.session = {"tsuru_token": "admin"}

    def test_should_require_login_to_rollback_app(self):
        assert issubclass(AppRollback, LoginRequiredView)

    @patch("requests.post")
    def test_post_with_valid_app_and_image(self, post):
        m = Mock(status_code=200, content="")
        post.return_value = m
        response = AppRollback.as_view()(
            self.request, app_name='test', image='localhost:3030/tsuru/app-test:v44')
        self.assertEqual(302, response.status_code)

    @patch("requests.post")
    def test_post_with_invalid_app_and_image(self, post):
        m = Mock(status_code=500, content="")
        post.return_value = m
        response = AppRollback.as_view()(
            self.request, app_name='test', image='localhost:3030/tsuru/app-test:v44')
        self.assertEqual('NOT OK', response.content)
