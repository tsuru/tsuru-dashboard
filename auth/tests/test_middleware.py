from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from auth.middleware import VerifyToken


class TestVerifyTokenMiddleware(TestCase):
    def test_process_exception(self):
        middleware = VerifyToken()

        request_mock = RequestFactory().get("/")
        exception = Exception()

        result = middleware.process_exception(request_mock, exception)
        self.assertEqual(result.url, reverse("logout"))
