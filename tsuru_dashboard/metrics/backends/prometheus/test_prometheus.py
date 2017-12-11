from django.test import TestCase
from tsuru_dashboard.metrics.backends.prometheus import Prometheus
from freezegun import freeze_time

from mock import patch
from datetime import datetime, timedelta
from time import mktime


class PrometheusTest(TestCase):
    def setUp(self):
        self.backend = Prometheus("http://url.com", query="key=value")

    @freeze_time("2012-04-01 16:32:15", tz_offset=0)
    @patch("requests.get")
    def test_mem_max(self, get_mock):
        self.backend.mem_max()
        start = datetime.now() - timedelta(hours=1)
        end = datetime.now()
        expected = self.backend.url
        expected += "/api/v1/query_range?"
        expected += "query=min(container_memory_usage_bytes{key=value})/1024/1024"
        expected += "&start={}&end={}&step={}".format(
            mktime(start.timetuple()),
            mktime(end.timetuple()),
            self.backend.resolution,
        )
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

    @freeze_time("2012-04-01 16:32:15", tz_offset=0)
    def test_date_range_by_days(self):
        backend = Prometheus(
            "http://url.com",
            query="key=value",
            date_range="1d",
        )
        self.assertEqual(backend.start, datetime.now() - timedelta(days=1))
        self.assertEqual(backend.end, datetime.now())

        backend = Prometheus(
            "http://url.com",
            query="key=value",
            date_range="3d",
        )
        self.assertEqual(backend.start, datetime.now() - timedelta(days=3))
        self.assertEqual(backend.end, datetime.now())

    @freeze_time("2012-04-01 16:32:15", tz_offset=0)
    def test_date_range_by_week(self):
        backend = Prometheus(
            "http://url.com",
            query="key=value",
            date_range="1w",
        )
        self.assertEqual(backend.start, datetime.now() - timedelta(days=7))
        self.assertEqual(backend.end, datetime.now())

        backend = Prometheus(
            "http://url.com",
            query="key=value",
            date_range="2w",
        )
        self.assertEqual(backend.start, datetime.now() - timedelta(days=14))
        self.assertEqual(backend.end, datetime.now())

    @freeze_time("2012-04-01 16:32:15", tz_offset=0)
    def test_resolution(self):
        backend = Prometheus(
            "http://url.com",
            query="key=value",
            date_range="1w",
        )
        resolution = (backend.end - backend.start).total_seconds() / 250
        self.assertEqual(backend.resolution, resolution)
