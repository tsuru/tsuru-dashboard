from django.test import TestCase

from tsuru_dashboard.metrics.backends.elasticsearch import AppBackend
from tsuru_dashboard.metrics.backends.elasticsearch import ElasticSearch, AppFilter, TsuruMetricsBackend, NodeMetricsBackend
from tsuru_dashboard.metrics.backends.elasticsearch import NET_AGGREGATION, NodesMetricsBackend

from mock import patch, Mock
import datetime
import json


class AppBackendTest(TestCase):
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

        backend = AppBackend(app, url="http://easearch.com")
        self.assertIsInstance(backend, ElasticSearch)

    @patch("requests.get")
    def test_envs_from_app(self, get_mock):
        get_mock.return_value = Mock(status_code=500)

        app = {"name": "appname", "envs": {"ELASTICSEARCH_HOST": "ble"}, "units": [{"ID": "id"}]}

        backend = AppBackend(app, 'token')
        self.assertIsInstance(backend, ElasticSearch)


class TsuruMetricsBackendTest(TestCase):
    def test_setup_backend(self):
        backend = TsuruMetricsBackend(filter=AppFilter(app="app_name"), date_range=u'2h')
        self.assertEqual(backend.filtered_query, AppFilter(app="app_name").query())
        self.assertEqual(backend.date_range, u'2h')


class NodesMetricsBackendTest(TestCase):
    def setUp(self):
        self.backend = NodesMetricsBackend(addrs=["127.0.0.1", "128.0.0.1"])
        self.index = ".measure-tsuru-{}*".format(datetime.datetime.utcnow().strftime("%Y.%m.%d"))
        self.aggregation = {
            "addrs": {
                "terms": {
                    "field": "addr.keyword",
                    "include": "127.0.0.1|128.0.0.1",
                    "size": 2
                },
                "aggs": {"avg": {"avg": {"field": "value"}}}
            }
        }

        self.net_aggregation = {
            "addrs": {
                "terms": {
                    "field": "addr.keyword",
                    "include": "127.0.0.1|128.0.0.1",
                    "size": 2
                },
                "aggs": NET_AGGREGATION["units"]["aggs"]
            }
        }

    @patch("requests.post")
    def test_cpu_max(self, post_mock):
        self.backend.cpu_max()
        url = "{}/{}/{}/_search".format(self.backend.url, self.index, "host_cpu_busy")
        post_mock.assert_called_with(url, data=json.dumps(self.backend.query(aggregation=self.aggregation)))

    @patch("requests.post")
    def test_cpu_wait(self, post_mock):
        self.backend.cpu_wait()
        url = "{}/{}/{}/_search".format(self.backend.url, self.index, "host_cpu_wait")
        post_mock.assert_called_with(url, data=json.dumps(self.backend.query(aggregation=self.aggregation)))

    @patch("requests.post")
    def test_load(self, post_mock):
        self.backend.load1()
        url = "{}/{}/{}/_search".format(self.backend.url, self.index, "host_load1")
        post_mock.assert_called_with(url, data=json.dumps(self.backend.query(aggregation=self.aggregation)))

        self.backend.load5()
        url = "{}/{}/{}/_search".format(self.backend.url, self.index, "host_load5")
        post_mock.assert_called_with(url, data=json.dumps(self.backend.query(aggregation=self.aggregation)))

        self.backend.load15()
        url = "{}/{}/{}/_search".format(self.backend.url, self.index, "host_load15")
        post_mock.assert_called_with(url, data=json.dumps(self.backend.query(aggregation=self.aggregation)))

    @patch("requests.post")
    def test_mem_max(self, post_mock):
        self.backend.mem_max()
        url = "{}/{}/{}/_search".format(self.backend.url, self.index, "host_mem_used")
        post_mock.assert_called_with(url, data=json.dumps(self.backend.query(aggregation=self.aggregation)))

    @patch("requests.post")
    def test_swap(self, post_mock):
        self.backend.swap()
        url = "{}/{}/{}/_search".format(self.backend.url, self.index, "host_swap_used")
        post_mock.assert_called_with(url, data=json.dumps(self.backend.query(aggregation=self.aggregation)))

    @patch("requests.post")
    def test_disk(self, post_mock):
        self.backend.disk()
        url = "{}/{}/{}/_search".format(self.backend.url, self.index, "host_disk_used")
        post_mock.assert_called_with(url, data=json.dumps(self.backend.query(aggregation=self.aggregation)))

    @patch("requests.post")
    def test_nettx(self, post_mock):
        self.backend.nettx()
        url = "{}/{}/{}/_search".format(self.backend.url, self.index, "host_nettx")
        post_mock.assert_called_with(url, data=json.dumps(
            self.backend.query(aggregation=self.net_aggregation)))

    @patch("requests.post")
    def test_netrx(self, post_mock):
        self.backend.netrx()
        url = "{}/{}/{}/_search".format(self.backend.url, self.index, "host_netrx")
        post_mock.assert_called_with(url, data=json.dumps(
            self.backend.query(aggregation=self.net_aggregation)))

    def test_process(self):
        data = {
            "hits": {
                "hits": [],
                "total": 899,
                "max_score": 0.0
            },
            "_shards": {
                "successful": 2,
                "failed": 0,
                "total": 2
            },
            "took": 1400,
            "aggregations": {
                "date": {
                    "buckets": [{
                        "addrs": {
                            "buckets": [{
                                "avg": {"value": 10.1},
                                "key": "127.0.0.1",
                                "doc_count": 15
                            }, {
                                "avg": {"value": 9.2},
                                "key": "128.0.0.1",
                                "doc_count": 15
                            }],
                            "sum_other_doc_count": 0,
                            "doc_count_error_upper_bound": 0
                        },
                        "key_as_string": "2015-07-21T19:35:00.000Z",
                        "key": 1437507300000,
                        "doc_count": 15
                    }, {
                        "addrs": {
                            "buckets": [{
                                "avg": {"value": 10},
                                "key": "127.0.0.1",
                                "doc_count": 15
                            }, {
                                "avg": {"value": 9.5},
                                "key": "128.0.0.1",
                                "doc_count": 15
                            }],
                            "sum_other_doc_count": 0,
                            "doc_count_error_upper_bound": 0
                        },
                        "key_as_string": "2015-07-21T19:36:00.000Z",
                        "key": 1437507360000,
                        "doc_count": 15
                    }]
                }
            }
        }
        expected = {
            "data": {
                "127.0.0.1": [[1437507300000, 20.2], [1437507360000, 20]],
                "128.0.0.1": [[1437507300000, 18.4], [1437507360000, 19]],
            },
            "min": 0,
            "max": 1
        }
        d = self.backend.process(data=data, formatter=lambda x: x * 2)
        self.assertDictEqual(d, expected)


class NodeMetricsBackendTest(TestCase):
    def setUp(self):
        self.backend = NodeMetricsBackend(addr="127.0.0.1")
        self.index = ".measure-tsuru-{}*".format(datetime.datetime.utcnow().strftime("%Y.%m.%d"))

    @patch("requests.post")
    def test_nettx(self, post_mock):
        self.backend.nettx()
        url = "{}/{}/{}/_search".format(self.backend.url, self.index, "host_nettx")
        post_mock.assert_called_with(url, data=json.dumps(self.backend.query(aggregation=NET_AGGREGATION)))

    @patch("requests.post")
    def test_netrx(self, post_mock):
        self.backend.netrx()
        url = "{}/{}/{}/_search".format(self.backend.url, self.index, "host_netrx")
        post_mock.assert_called_with(url, data=json.dumps(self.backend.query(aggregation=NET_AGGREGATION)))

    @patch("requests.post")
    def test_mem_max(self, post_mock):
        self.backend.process = Mock()
        self.backend.mem_max()
        url = "{}/{}/{}/_search".format(self.backend.url, self.index, "host_mem_used")
        post_mock.assert_called_with(url, data=json.dumps(self.backend.query()))

    @patch("requests.post")
    def test_cpu_max(self, post_mock):
        aggregation = {
            "stats": {
                "terms": {"field": "_type"},
                "aggs": {"stats": {"stats": {"field": "value"}}}
            }
        }
        self.backend.cpu_max()
        url = "{}/{}/{}/_search".format(
            self.backend.url, self.index, "host_cpu_user,host_cpu_sys,host_cpu_wait")
        post_mock.assert_called_with(url, data=json.dumps(self.backend.query(aggregation=aggregation)))

    @patch("requests.post")
    def test_load(self, post_mock):
        aggregation = {
            "stats": {
                "terms": {"field": "_type"},
                "aggs": {"stats": {"stats": {"field": "value"}}}
            }
        }
        self.backend.load()
        url = "{}/{}/{}/_search".format(self.backend.url, self.index, "host_load1,host_load5,host_load15")
        post_mock.assert_called_with(url, data=json.dumps(self.backend.query(aggregation=aggregation)))

    @patch("requests.post")
    def test_swap(self, post_mock):
        aggregation = {
            "stats": {
                "terms": {"field": "_type"},
                "aggs": {"stats": {"stats": {"field": "value"}}}
            }
        }
        self.backend.swap()
        url = "{}/{}/{}/_search".format(self.backend.url, self.index, "host_swap_used,host_swap_total")
        post_mock.assert_called_with(url, data=json.dumps(self.backend.query(aggregation=aggregation)))

    @patch("requests.post")
    def test_disk(self, post_mock):
        aggregation = {
            "stats": {
                "terms": {"field": "_type"},
                "aggs": {"stats": {"stats": {"field": "value"}}}
            }
        }
        self.backend.disk()
        url = "{}/{}/{}/_search".format(self.backend.url, self.index, "host_disk_used,host_disk_total")
        post_mock.assert_called_with(url, data=json.dumps(self.backend.query(aggregation=aggregation)))

    def test_load_process(self):
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
                                "buckets": [
                                    {
                                        "stats": {
                                            "avg": 0.021
                                        },
                                        "key": "host_load1"
                                    },
                                    {
                                        "stats": {
                                            "avg": 0.025
                                        },
                                        "key": "host_load5"
                                    },
                                    {
                                        "stats": {
                                            "avg": 0.015
                                        },
                                        "key": "host_load15"
                                    }
                                ]
                            }
                        },
                        {
                            "key_as_string": "2015-07-21T19:36:00.000Z",
                            "key": 1437507360000,
                            "doc_count": 9,
                            "stats": {
                                "buckets": [
                                    {
                                        "stats": {
                                            "avg": 0.020
                                        },
                                        "key": "host_load1"
                                    },
                                    {
                                        "stats": {
                                            "avg": 0.026
                                        },
                                        "key": "host_load5"
                                    },
                                    {
                                        "stats": {
                                            "avg": 0.014
                                        },
                                        "key": "host_load15"
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        }
        expected = {
            "data": {
                "load1": [[1437507300000, 0.021], [1437507360000, 0.020]],
                "load5": [[1437507300000, 0.025], [1437507360000, 0.026]],
                "load15": [[1437507300000, 0.015], [1437507360000, 0.014]],
            },
            "min": 0,
            "max": 1
        }
        d = self.backend.base_process(data, self.backend.load_process)
        self.assertDictEqual(d, expected)

    def test_cpu_max_process(self):
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
                                "buckets": [
                                    {
                                        "stats": {
                                            "avg": 0.021
                                        },
                                        "key": "host_cpu_sys"
                                    },
                                    {
                                        "stats": {
                                            "avg": 0.015
                                        },
                                        "key": "host_cpu_user"
                                    },
                                    {
                                        "stats": {
                                            "avg": 0.001
                                        },
                                        "key": "host_cpu_wait"
                                    }
                                ]
                            }
                        },
                        {
                            "key_as_string": "2015-07-21T19:36:00.000Z",
                            "key": 1437507360000,
                            "doc_count": 9,
                            "stats": {
                                "buckets": [
                                    {
                                        "stats": {
                                            "avg": 0.020
                                        },
                                        "key": "host_cpu_sys"
                                    },
                                    {
                                        "stats": {
                                            "avg": 0.016
                                        },
                                        "key": "host_cpu_user"
                                    },
                                    {
                                        "stats": {
                                            "avg": 0.000
                                        },
                                        "key": "host_cpu_wait"
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        }
        expected = {
            "data": {
                "sys": [[1437507300000, 2.1], [1437507360000, 2.0]],
                "user": [[1437507300000, 1.5], [1437507360000, 1.6]],
                "wait": [[1437507300000, 0.1], [1437507360000, 0]],
            },
            "min": 0,
            "max": 1
        }
        d = self.backend.base_process(data, self.backend.cpu_max_process)
        self.assertDictEqual(d, expected)
