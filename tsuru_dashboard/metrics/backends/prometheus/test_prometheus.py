from django.test import TestCase
from tsuru_dashboard.metrics.backends.prometheus import Prometheus, AppBackend
from freezegun import freeze_time

from mock import patch, Mock
from datetime import datetime, timedelta
from time import mktime


class AppBackendTest(TestCase):
    def setUp(self):
        self.backend = AppBackend({"name": "myapp"}, "http://url.com", process_name="myprocess")

    @freeze_time("2012-04-01 16:32:15", tz_offset=0)
    @patch("requests.get")
    def test_mem_max(self, get_mock):
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = {
            "data": {
                "result": [{
                    "values": [],
                }],
            },
        }
        get_mock.return_value = response_mock

        self.backend.mem_max()
        start = datetime.now() - timedelta(hours=1)
        end = datetime.now()
        expected_url = self.backend.url + "/api/v1/query_range"
        expected_params = {
            'query': 'min(container_memory_usage_bytes{container_name=~"myapp-myprocess.*",})/1024/1024 or min(container_memory_usage_bytes{container_name="POD",pod_name=~"myapp-myprocess.*",})/1024/1024 or min(container_memory_usage_bytes{container_label_app_name="myapp",container_label_app_process="myprocess",})/1024/1024',
            'start': mktime(start.timetuple()),
            'end': mktime(end.timetuple()),
            'step': self.backend.resolution,
        }
        get_mock.assert_called_with(expected_url, params=expected_params)


class PrometheusTest(TestCase):
    def setUp(self):
        self.backend = Prometheus("http://url.com")

    @freeze_time("2012-04-01 16:32:15", tz_offset=0)
    def test_default_date_range(self):
        backend = Prometheus(
            "http://url.com",
        )
        self.assertEqual(backend.start, datetime.now() - timedelta(hours=1))
        self.assertEqual(backend.end, datetime.now())

    @freeze_time("2012-04-01 16:32:15", tz_offset=0)
    def test_hour_date_range(self):
        backend = Prometheus(
            "http://url.com",
            date_range="1h",
        )
        self.assertEqual(backend.start, datetime.now() - timedelta(hours=1))
        self.assertEqual(backend.end, datetime.now())

        backend = Prometheus(
            "http://url.com",
            date_range="3h",
        )
        self.assertEqual(backend.start, datetime.now() - timedelta(hours=3))
        self.assertEqual(backend.end, datetime.now())

    @freeze_time("2012-04-01 16:32:15", tz_offset=0)
    def test_date_range_by_days(self):
        backend = Prometheus(
            "http://url.com",
            date_range="1d",
        )
        self.assertEqual(backend.start, datetime.now() - timedelta(days=1))
        self.assertEqual(backend.end, datetime.now())

        backend = Prometheus(
            "http://url.com",
            date_range="3d",
        )
        self.assertEqual(backend.start, datetime.now() - timedelta(days=3))
        self.assertEqual(backend.end, datetime.now())

    @freeze_time("2012-04-01 16:32:15", tz_offset=0)
    def test_date_range_by_week(self):
        backend = Prometheus(
            "http://url.com",
            date_range="1w",
        )
        self.assertEqual(backend.start, datetime.now() - timedelta(days=7))
        self.assertEqual(backend.end, datetime.now())

        backend = Prometheus(
            "http://url.com",
            date_range="2w",
        )
        self.assertEqual(backend.start, datetime.now() - timedelta(days=14))
        self.assertEqual(backend.end, datetime.now())

    @freeze_time("2012-04-01 16:32:15", tz_offset=0)
    def test_resolution(self):
        backend = Prometheus(
            "http://url.com",
            date_range="1w",
        )
        resolution = (backend.end - backend.start).total_seconds() / 250
        self.assertEqual(backend.resolution, resolution)
