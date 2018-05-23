from django.test import TestCase
from django.test.client import RequestFactory

from tsuru_dashboard.auth.views import get_oauth_redirect_url


class UtilsTest(TestCase):

    def test_get_oauth_redirect_url_when_request_is_insecure_should_be_scheme_equals_to_http(self):
        request = RequestFactory().get('/')
        request.META['HTTP_HOST'] = 'tsuru.local'

        redirect_oauth_url = get_oauth_redirect_url(request)

        self.assertEqual(redirect_oauth_url, 'http://tsuru.local/auth/callback/')

    def test_get_oauth_redirect_url_when_request_is_secure_should_be_scheme_equals_to_https(self):
        request = RequestFactory().get('/', secure=True)
        request.META['HTTP_HOST'] = 'tsuru.local'

        redirect_oauth_url = get_oauth_redirect_url(request)

        self.assertEqual(redirect_oauth_url, 'https://tsuru.local/auth/callback/')

    def test_get_oauth_redirect_url_when_connection_from_enduser_to_proxy_is_secure_should_be_scheme_equals_to_https(self):
        request = RequestFactory().get('/')
        request.META['HTTP_HOST'] = 'tsuru.local'
        request.META['HTTP_X_FORWARDED_PROTO'] = 'https'

        redirect_oauth_url = get_oauth_redirect_url(request)

        self.assertEqual(redirect_oauth_url, 'https://tsuru.local/auth/callback/')

    def test_get_oauth_redirect_url_when_header_host_is_undefined_should_use_fallback_server_name(self):
        request = RequestFactory().get('/')
        request.META['SERVER_NAME'] = 'localhost:8000'

        redirect_oauth_url = get_oauth_redirect_url(request)

        self.assertEqual(redirect_oauth_url, 'http://localhost:8000/auth/callback/')
