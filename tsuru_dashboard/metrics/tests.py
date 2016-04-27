from django.test import TestCase
from django.test.client import RequestFactory

from tsuru_dashboard import settings
from tsuru_dashboard.metrics.backend import ElasticSearch, AppFilter, ComponentFilter
from tsuru_dashboard.metrics.backend import get_backend, MetricNotEnabled, NET_AGGREGATION
from tsuru_dashboard.metrics import views

from mock import patch, Mock
import json
import datetime


class MetricViewTest(TestCase):
    def request(self, string_params=""):
        request = RequestFactory().get("/ble/" + string_params)
        request.session = {"tsuru_token": "token"}
        return request

    @patch("requests.get")
    def test_get_app(self, get_mock):
        response_mock = Mock()
        response_mock.json.return_value = {}
        get_mock.return_value = response_mock

        view = views.Metric()
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

        view = views.Metric()
        view.request = self.request()
        envs = view.get_envs(self.request(), "app_name")

        self.assertDictEqual(envs, {"VAR": "value"})
        url = "{}/apps/app_name/env".format(settings.TSURU_HOST)
        headers = {"authorization": "token"}
        get_mock.assert_called_with(url, headers=headers)

    @patch("tsuru_dashboard.metrics.backend.get_backend")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_get_app_metric(self, token_mock, get_backend_mock):
        token_mock.return_value = True
        backend_mock = Mock()
        backend_mock.cpu_max.return_value = {}
        get_backend_mock.return_value = backend_mock

        v = views.Metric

        original_get_app = v.get_app
        v.get_app = Mock()
        v.get_app.return_value = {}

        original_get_envs = v.get_envs
        v.get_envs = Mock()
        v.get_envs.return_value = {}
        view = v.as_view()

        def cleanup():
            v.get_app = original_get_app
            v.get_envs = original_get_envs

        self.addCleanup(cleanup)

        request = self.request("?metric=cpu_max&date_range=2h/h&interval=30m&process_name=web")
        response = view(request, target_name="app_name", target_type="app")

        self.assertEqual(response.status_code, 200)
        get_backend_mock.assert_called_with(
            app={'envs': {}}, token='token', date_range=u'2h/h', process_name=u'web')
        backend_mock.cpu_max.assert_called_with(interval=u'30m')

    @patch("tsuru_dashboard.metrics.backend.get_backend")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_get_component_metric(self, token_mock, get_backend_mock):
        token_mock.return_value = True
        backend_mock = Mock()
        backend_mock.cpu_max.return_value = {}
        get_backend_mock.return_value = backend_mock

        v = views.Metric

        original_get_app = v.get_app
        v.get_app = Mock()
        v.get_app.return_value = {}

        original_get_envs = v.get_envs
        v.get_envs = Mock()
        v.get_envs.return_value = {}
        view = v.as_view()

        def cleanup():
            v.get_app = original_get_app
            v.get_envs = original_get_envs

        self.addCleanup(cleanup)

        request = self.request("?metric=cpu_max&date_range=2h/h&interval=30m")
        response = view(request, target_name="comp_name", target_type="component")

        self.assertEqual(response.status_code, 200)
        get_backend_mock.assert_called_with(
            component_name="comp_name", token='token', date_range=u'2h/h', app=None)
        backend_mock.cpu_max.assert_called_with(interval=u'30m')

    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_get_bad_request(self, token_mock):
        request = RequestFactory().get("")
        request.session = {"tsuru_token": "token"}
        token_mock.return_value = True

        v = views.Metric
        view = v.as_view()

        response = view(request, app_name="app_name")

        self.assertEqual(response.status_code, 400)


class GetBackendTest(TestCase):
    @patch("requests.get")
    def test_envs_from_api(self, get_mock):
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = {
            "METRICS_BACKEND": "logstash",
            "METRICS_ELASTICSEARCH_HOST": "http://easearch.com",
            "METRICS_LOGSTASH_HOST": "logstash.com"
        }
        get_mock.return_value = response_mock

        app = {"name": "appname", "units": [{"ProcessName": "web"}]}

        backend = get_backend(app, 'token')
        self.assertIsInstance(backend, ElasticSearch)

    @patch("requests.get")
    def test_envs_from_app(self, get_mock):
        get_mock.return_value = Mock(status_code=500)

        app = {"name": "appname", "envs": {"ELASTICSEARCH_HOST": "ble"}, "units": [{"ID": "id"}]}

        backend = get_backend(app, 'token')
        self.assertIsInstance(backend, ElasticSearch)

    @patch("requests.get")
    def test_without_metrics(self, get_mock):
        get_mock.return_value = Mock(status_code=404)
        app = {"name": "appname"}

        with self.assertRaises(MetricNotEnabled):
            get_backend(app, 'token')


class ElasticSearchTest(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.es = ElasticSearch("http://url.com", AppFilter(app="app_name").query())
        self.index = ".measure-tsuru-{}".format(datetime.datetime.utcnow().strftime("%Y.%m.%d"))

    @patch("requests.post")
    def test_cpu_max(self, post_mock):
        self.es.process = Mock()
        self.es.cpu_max()
        url = "{}/{}/{}/_search".format(self.es.url, self.index, "cpu_max")
        post_mock.assert_called_with(url, data=json.dumps(self.es.query()))

    @patch("requests.post")
    def test_mem_max(self, post_mock):
        self.es.process = Mock()
        self.es.mem_max()
        url = "{}/{}/{}/_search".format(self.es.url, self.index, "mem_max")
        post_mock.assert_called_with(url, data=json.dumps(self.es.query()))

    @patch("requests.post")
    def test_swap(self, post_mock):
        self.es.process = Mock()
        self.es.swap()
        url = "{}/{}/{}/_search".format(self.es.url, self.index, "swap")
        post_mock.assert_called_with(url, data=json.dumps(self.es.query()))

    @patch("requests.post")
    def test_units(self, post_mock):
        self.es.units()
        url = "{}/{}/{}/_search".format(self.es.url, self.index, "cpu_max")
        aggregation = {"units": {"cardinality": {"field": "host.raw"}}}
        post_mock.assert_called_with(url, data=json.dumps(self.es.query(aggregation=aggregation)))

    @patch("requests.post")
    def test_requests_min(self, post_mock):
        self.es.requests_min()
        url = "{}/{}/{}/_search".format(self.es.url, self.index, "response_time")
        aggregation = {"sum": {"sum": {"field": "count"}}}
        post_mock.assert_called_with(url, data=json.dumps(self.es.query(aggregation=aggregation)))

    @patch("requests.post")
    def test_response_time(self, post_mock):
        self.es.response_time()
        url = "{}/{}/{}/_search".format(self.es.url, self.index, "response_time")
        aggregation = {
            "stats": {"stats": {"field": "value"}},
            "percentiles": {"percentiles": {"field": "value"}}
        }
        post_mock.assert_called_with(url, data=json.dumps(self.es.query(aggregation=aggregation)))

    @patch("requests.post")
    def test_http_methods(self, post_mock):
        self.es.http_methods()
        url = "{}/{}/{}/_search".format(self.es.url, self.index, "response_time")
        aggregation = {"method": {"terms": {"field": "method"}}}
        post_mock.assert_called_with(url, data=json.dumps(self.es.query(aggregation=aggregation)))

    @patch("requests.post")
    def test_status_code(self, post_mock):
        self.es.status_code()
        url = "{}/{}/{}/_search".format(self.es.url, self.index, "response_time")
        aggregation = {"status_code": {"terms": {"field": "status_code"}}}
        post_mock.assert_called_with(url, data=json.dumps(self.es.query(aggregation=aggregation)))

    @patch("requests.post")
    def test_top_slow(self, post_mock):
        self.es.top_slow()
        url = "{}/{}/{}/_search".format(self.es.url, self.index, "response_time")
        aggregation = {
            "top": {
                "terms": {
                    "script": "doc['method'].value +'U'+doc['path.raw'].value +'U'+doc['status_code'].value"
                },
                "aggs": {"max": {"max": {"field": "value"}}}
            }
        }
        post_mock.assert_called_with(url, data=json.dumps(self.es.query(aggregation=aggregation)))

    @patch("requests.post")
    def test_connections(self, post_mock):
        self.es.connections()
        url = "{}/{}/{}/_search".format(self.es.url, self.index, "connection")
        aggregation = {"connection": {"terms": {"field": "connection.raw"}}}
        post_mock.assert_called_with(url, data=json.dumps(self.es.query(aggregation=aggregation)))

    @patch("requests.post")
    def test_netrx(self, post_mock):
        self.es.netrx()
        url = "{}/{}/{}/_search".format(self.es.url, self.index, "netrx")
        post_mock.assert_called_with(url, data=json.dumps(self.es.query(aggregation=NET_AGGREGATION)))

    @patch("requests.post")
    def test_nettx(self, post_mock):
        self.es.nettx()
        url = "{}/{}/{}/_search".format(self.es.url, self.index, "nettx")
        post_mock.assert_called_with(url, data=json.dumps(self.es.query(aggregation=NET_AGGREGATION)))

    def test_process(self):
        data = {
            "took": 86,
            "timed_out": False,
            "_shards": {
                "total": 266,
                "successful": 266,
                "failed": 0
            },
            "hits": {
                "total": 644073,
                "max_score": 0,
                "hits": []
            },
            "aggregations": {
                "date": {
                    "buckets": [
                        {
                            "key_as_string": "2015-07-21T19:35:00.000Z",
                            "key": 1437507300000,
                            "doc_count": 9,
                            "stats": {
                                "min": 97517568,
                                "max": 97517568,
                                "avg": 97517568
                            }
                        },
                        {
                            "key_as_string": "2015-07-21T19:36:00.000Z",
                            "key": 1437507360000,
                            "doc_count": 9,
                            "stats": {
                                "min": 97517568,
                                "max": 97517568,
                                "avg": 97517568
                            }
                        }
                    ]
                }
            }
        }
        expected = {
            "data": {
                "max": [[1437507300000, 97517568], [1437507360000, 97517568]],
                "min": [[1437507300000, 97517568], [1437507360000, 97517568]],
                "avg": [[1437507300000, 97517568], [1437507360000, 97517568]],
            },
            "min": 97517568,
            "max": 97517569
        }
        d = self.es.process(data)
        self.assertDictEqual(d, expected)

    def test_process_custom_formatter(self):
        data = {
            "took": 86,
            "timed_out": False,
            "_shards": {
                "total": 266,
                "successful": 266,
                "failed": 0
            },
            "hits": {
                "total": 644073,
                "max_score": 0,
                "hits": []
            },
            "aggregations": {
                "date": {
                    "buckets": [
                        {
                            "key_as_string": "2015-07-21T19:35:00.000Z",
                            "key": 1437507300000,
                            "doc_count": 9,
                            "stats": {
                                "min": 97517568,
                                "max": 97517568,
                                "avg": 97517568
                            }
                        },
                        {
                            "key_as_string": "2015-07-21T19:36:00.000Z",
                            "key": 1437507360000,
                            "doc_count": 9,
                            "stats": {
                                "min": 97517568,
                                "max": 97517568,
                                "avg": 97517568
                            }
                        }
                    ]
                }
            }
        }
        expected = {
            "data": {
                "max": [[1437507300000, 93], [1437507360000, 93]],
                "min": [[1437507300000, 93], [1437507360000, 93]],
                "avg": [[1437507300000, 93], [1437507360000, 93]],
            },
            "min": 93,
            "max": 94
        }
        d = self.es.process(data, formatter=lambda x: x / (1024 * 1024))
        self.assertDictEqual(d, expected)

    def test_process_no_aggregation(self):
        data = {
            "took": 1,
            "timed_out": False,
            "_shards": {
                "total": 0,
                "successful": 0,
                "failed": 0
            },
            "hits": {
                "total": 0,
                "max_score": 0,
                "hits": []
            }
        }
        expected = {'data': {}, 'max': 1, 'min': 0}
        d = self.es.process(data, formatter=lambda x: x / (1024 * 1024))
        self.assertDictEqual(d, expected)

    def test_unit_process_no_aggregation(self):
        data = {
            "took": 1,
            "timed_out": False,
            "_shards": {
                "total": 0,
                "successful": 0,
                "failed": 0
            },
            "hits": {
                "total": 0,
                "max_score": 0,
                "hits": []
            }
        }
        expected = {'data': {}, 'max': 1, 'min': 0}
        d = self.es.base_process(data, self.es.units_process)
        self.assertDictEqual(d, expected)

    def test_request_min_process_no_aggregation(self):
        data = {
            "took": 1,
            "timed_out": False,
            "_shards": {
                "total": 0,
                "successful": 0,
                "failed": 0
            },
            "hits": {
                "total": 0,
                "max_score": 0,
                "hits": []
            }
        }
        expected = {'data': {}, 'max': 1, 'min': 0}
        d = self.es.base_process(data, self.es.requests_min_process)
        self.assertDictEqual(d, expected)

    def test_connections_process_no_aggregation(self):
        data = {
            "took": 1,
            "timed_out": False,
            "_shards": {
                "total": 0,
                "successful": 0,
                "failed": 0
            },
            "hits": {
                "total": 0,
                "max_score": 0,
                "hits": []
            }
        }
        expected = {'data': {}, 'max': 1, 'min': 0}
        d = self.es.base_process(data, self.es.connections_process)
        self.assertDictEqual(d, expected)


class ElasticSearchFilterTest(TestCase):
    def test_app_filters(self):
        expected_filter = {
            "bool": {
                "must": [
                    {
                        "bool": {
                            "should": [
                                {"term": {"app": "app_name"}},
                                {"term": {"app.raw": "app_name"}},
                            ]
                        },
                    },
                    {
                        "range": {
                            "@timestamp": {
                                "gte": "now-1h",
                                "lt": "now"
                            }
                        }
                    },
                    {
                        "bool": {
                            "should": [
                                {"term": {"process": "process_name"}},
                                {"term": {"process.raw": "process_name"}}
                            ]
                        }
                    }
                ]
            }
        }
        filter = AppFilter(app="app_name", process_name="process_name").filter
        self.assertDictEqual(filter, expected_filter)

    def test_component_filters(self):
        expected_filter = {
            "bool": {
                "must": [
                    {
                        "bool": {
                            "should": [
                                {"term": {"container": "comp_name"}},
                                {"term": {"container.raw": "comp_name"}},
                            ]
                        },
                    },
                    {
                        "range": {
                            "@timestamp": {
                                "gte": "now-1h",
                                "lt": "now"
                            }
                        }
                    },
                ]
            }
        }
        filter = ComponentFilter(component="comp_name").filter
        self.assertDictEqual(filter, expected_filter)
