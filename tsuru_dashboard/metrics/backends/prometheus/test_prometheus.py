from django.test import TestCase
from tsuru_dashboard.metrics.backends.prometheus import Prometheus
from mock import patch


class PrometheusTest(TestCase):
    def setUp(self):
        self.backend = Prometheus("http://url.com", query="key=value")

    @patch("requests.get")
    def test_mem_max(self, get_mock):
        self.backend.mem_max()
        expected = self.backend.url
        expected += "/api/v1/query_range?"
        expected += "query=min(container_memory_usage_bytes{key=value})/1024/1024"
        expected += "&start=1473209927.011&end=1473213527.011&step=14"
        get_mock.assert_called_with(expected)
