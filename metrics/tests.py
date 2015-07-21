from django.test import TestCase
from metrics.backend import ElasticSearch

from mock import patch


class ElasticSearchTest(TestCase):
    def setUp(self):
        self.es = ElasticSearch("http://url.com", "index", "app")

    @patch("requests.post")
    def test_cpu_max(self, post_mock):
        self.es.cpu_max()
        post_mock.assert_called_with(self.es.url, data=self.es.query(key="cpu_max"))

    @patch("requests.post")
    def test_mem_max(self, post_mock):
        self.es.mem_max()
        post_mock.assert_called_with(self.es.url, data=self.es.query(key="mem_max"))

    @patch("requests.post")
    def test_units(self, post_mock):
        self.es.units()
        post_mock.assert_called_with(self.es.url, data=self.es.query(key="cpu_max"))

    @patch("requests.post")
    def test_requests_min(self, post_mock):
        self.es.requests_min()
        post_mock.assert_called_with(self.es.url, data=self.es.query(key="response_time"))

    @patch("requests.post")
    def test_response_time(self, post_mock):
        self.es.response_time()
        post_mock.assert_called_with(self.es.url, data=self.es.query(key="response_time"))

    @patch("requests.post")
    def test_connections(self, post_mock):
        self.es.connections()
        post_mock.assert_called_with(self.es.url, data=self.es.query(key="connection"))
