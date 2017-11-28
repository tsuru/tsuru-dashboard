from django.test import TestCase
from tsuru_dashboard.metrics.backends import base
from mock import patch, Mock
from tsuru_dashboard import settings


class BackendTest(TestCase):
    @patch("requests.get")
    def test_envs_from_api(self, get_mock):
        data = {
            "METRICS_BACKEND": "logstash",
            "METRICS_ELASTICSEARCH_HOST": "http://easearch.com",
            "METRICS_LOGSTASH_HOST": "logstash.com"
        }
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = data
        get_mock.return_value = response_mock

        app = {"name": "appname", "units": [{"ProcessName": "web"}]}

        envs = base.get_envs_from_api(app, 'token')
        self.assertDictEqual(envs, data)

    def test_set_destination_hostname(self):
        tests = [
            ("", ""),
            ("x", "x"),
            ("127.0.0.9", "127\.0\.0\.9"),
            ("127.0.0.9:1234", "127\.0\.0\.9:1234"),
            ("127.0.0.1", "127\.0\.0\.1\(.*localhost\)"),
            ("127.0.0.1:1234", "127\.0\.0\.1:1234\(.*localhost\)"),
        ]
        settings.RESOLVE_CONNECTION_HOSTS = False
        for v1, v2 in tests:
            self.assertEqual(base.set_destination_hostname(v1), v1)
        settings.RESOLVE_CONNECTION_HOSTS = True
        for v1, v2 in tests:
            self.assertRegexpMatches(base.set_destination_hostname(v1), v2)
        settings.RESOLVE_CONNECTION_HOSTS = False
