from django.test import TestCase
from tsuru_dashboard.metrics.backends.elasticsearch import ElasticSearch, AppFilter, NET_AGGREGATION
from mock import patch, Mock
import datetime
import json


class ElasticSearchTest(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.es = ElasticSearch("http://url.com", AppFilter(app="app_name").query())
        self.index = ".measure-tsuru-{}*".format(datetime.datetime.utcnow().strftime("%Y.%m.%d"))

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
        aggregation = {"units": {"cardinality": {"field": "host.keyword"}}}
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
        query = {
            "query": self.es.filtered_query,
            "size": 0,
            "aggs": {
                "top": {
                    "terms": {
                        "script": "doc['method'].value +'|-o-|'+doc['path.keyword'].value +'|-o-|'+doc['status_code'].value",
                        "order": {
                            "stats.max": "desc"
                        }
                    },
                    "aggs": {
                        "stats": {"stats": {"field": "value"}},
                        "percentiles": {"percentiles": {"field": "value"}},
                        "max": {
                            "top_hits": {
                                "sort": [{"value": {"order": "desc"}}],
                                "size": 1
                            }
                        }
                    }
                }
            }
        }
        post_mock.assert_called_with(url, data=json.dumps(query))

    @patch("requests.post")
    def test_connections(self, post_mock):
        self.es.connections()
        url = "{}/{}/{}/_search".format(self.es.url, self.index, "connection")
        aggregation = {"connection": {"terms": {"field": "connection.keyword"}}}
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
