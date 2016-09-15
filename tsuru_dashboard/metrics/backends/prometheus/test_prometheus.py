from django.test import TestCase
from tsuru_dashboard.metrics.backends.prometheus import Prometheus
from freezegun import freeze_time

from mock import patch
from datetime import datetime, timedelta


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

    @freeze_time("2012-04-01 16:32:15", tz_offset=0)
    def test_default_date_range(self):
        backend = Prometheus(
            "http://url.com",
            query="key=value",
        )
        self.assertEqual(backend.start, datetime.now() - timedelta(hours=1))
        self.assertEqual(backend.end, datetime.now())

    @freeze_time("2012-04-01 16:32:15", tz_offset=0)
    def test_hour_date_range(self):
        backend = Prometheus(
            "http://url.com",
            query="key=value",
            date_range="1h",
        )
        self.assertEqual(backend.start, datetime.now() - timedelta(hours=1))
        self.assertEqual(backend.end, datetime.now())

        backend = Prometheus(
            "http://url.com",
            query="key=value",
            date_range="3h",
        )
        self.assertEqual(backend.start, datetime.now() - timedelta(hours=3))
        self.assertEqual(backend.end, datetime.now())
