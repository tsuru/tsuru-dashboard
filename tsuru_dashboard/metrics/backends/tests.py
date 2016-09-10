from django.test import TestCase
from tsuru_dashboard import settings
from tsuru_dashboard.metrics.backends import get_app, get_envs
from mock import patch, Mock


class BackendsTest(TestCase):
    @patch("requests.get")
    def test_get_app(self, get_mock):
        response_mock = Mock()
        response_mock.json.return_value = {}
        get_mock.return_value = response_mock

        app = get_app("app_name", "token")

        self.assertDictEqual(app, {})
        url = "{}/apps/app_name".format(settings.TSURU_HOST)
        headers = {"authorization": "token"}
        get_mock.assert_called_with(url, headers=headers)

    @patch("requests.get")
    def test_get_envs(self, get_mock):
        env_mock = [{"name": "VAR", "value": "value"}]
        response_mock = Mock()
        response_mock.json.return_value = env_mock
        get_mock.return_value = response_mock

        envs = get_envs("app_name", "token")

        self.assertDictEqual(envs, {"VAR": "value"})
        url = "{}/apps/app_name/env".format(settings.TSURU_HOST)
        headers = {"authorization": "token"}
        get_mock.assert_called_with(url, headers=headers)
