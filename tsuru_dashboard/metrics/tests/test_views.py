from django.test import TestCase
from django.test.client import RequestFactory
from tsuru_dashboard import settings
from tsuru_dashboard.metrics import views
from mock import patch, Mock
import httpretty
import json


class AppMetricViewTest(TestCase):
    def request(self, string_params=""):
        request = RequestFactory().get("/ble/" + string_params)
        request.session = {"tsuru_token": "token"}
        return request

    @patch("requests.get")
    def test_get_app(self, get_mock):
        response_mock = Mock()
        response_mock.json.return_value = {}
        get_mock.return_value = response_mock

        view = views.AppMetric()
        view.request = self.request()
        app = view.get_app("app_name")

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

        view = views.AppMetric()
        view.request = self.request()
        envs = view.get_envs(self.request(), "app_name")

        self.assertDictEqual(envs, {"VAR": "value"})
        url = "{}/apps/app_name/env".format(settings.TSURU_HOST)
        headers = {"authorization": "token"}
        get_mock.assert_called_with(url, headers=headers)

    @patch("requests.post")
    @patch("requests.get")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_get_app_metric(self, token_mock, get_mock, post_mock):
        response_mock = Mock(status_code=200)
        response_mock.json.side_effect = [
            {"name": "app_name"}, {}, {"METRICS_ELASTICSEARCH_HOST": "http://easearch.com"}
        ]
        get_mock.return_value = response_mock
        token_mock.return_value = True
        view = views.AppMetric.as_view()

        request = self.request("?metric=cpu_max&date_range=2h/h&interval=30m&process_name=web")
        response = view(request, target="app_name")
        self.assertEqual(response.status_code, 200)


class ComponentMetricViewTest(TestCase):
    def request(self, string_params=""):
        request = RequestFactory().get("/ble/" + string_params)
        request.session = {"tsuru_token": "token"}
        return request

    @patch("requests.post")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_get_component_metric(self, token_mock, post_mock):
        token_mock.return_value = True
        view = views.ComponentMetric.as_view()

        request = self.request("?metric=cpu_max&date_range=2h/h&interval=30m")
        response = view(request, target="comp_name")

        self.assertEqual(response.status_code, 200)


class MetricViewTest(TestCase):
    def request(self, string_params=""):
        request = RequestFactory().get("/ble/" + string_params)
        request.session = {"tsuru_token": "token"}
        return request

    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_get_bad_request(self, token_mock):
        request = RequestFactory().get("")
        request.session = {"tsuru_token": "token"}
        token_mock.return_value = True
        view = views.Metric.as_view()

        response = view(request, name="app_name")

        self.assertEqual(response.status_code, 400)


class PoolMetricViewTest(TestCase):

    def setUp(self):
        self.api_url = "{}/docker/node".format(settings.TSURU_HOST)
        data = {
            "machines": None,
            "nodes": [
                {"Address": "http://128.0.0.1:4243",
                    "Metadata": {"LastSuccess": "2014-08-01T14:09:40-03:00",
                                 "pool": "theonepool"},
                 "Status": "ready"},
                {"Address": "http://127.0.0.1:2375",
                 "Metadata": {"LastSuccess": "2014-08-01T14:09:40-03:00",
                              "pool": "theonepool"},
                 "Status": "ready"},
                {"Address": "http://myserver.com:2375",
                 "Metadata": {"LastSuccess": "2014-08-01T14:09:40-03:00",
                              "pool": "anotherpool"},
                 "Status": "ready"},
            ],
        }
        self.api_body = json.dumps(data)
        self.maxDiff = None
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}

    @httpretty.activate
    def test_get_pool_nodes_addrs(self):
        httpretty.register_uri(httpretty.GET, self.api_url, body=self.api_body)
        view = views.PoolMetric(request=self.request)
        addrs = view.get_pool_nodes("theonepool")
        self.assertEqual(addrs, ["128.0.0.1", "127.0.0.1"])

    @httpretty.activate
    @patch("requests.post")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_get_pool_metric(self, token_is_valid, post_mock):
        token_is_valid.return_value = True
        httpretty.register_uri(httpretty.GET, self.api_url, body=self.api_body)
        view = views.PoolMetric.as_view()
        request = RequestFactory().get("/ble/?metric=cpu_max&date_range=2h/h&interval=30m")
        request.session = {"tsuru_token": "token"}
        response = view(request, target="theonepool")

        self.assertEqual(response.status_code, 200)
