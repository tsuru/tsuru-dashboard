from django.test import TestCase
from tsuru_dashboard.metrics.backends import base
from mock import patch, Mock


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
