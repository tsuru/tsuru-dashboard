from django.test import TestCase
from django.test.client import RequestFactory
from tsuru_dashboard import settings
from tsuru_dashboard.metrics import views
from mock import patch, Mock


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
