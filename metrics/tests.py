from django.test import TestCase
from metrics.backend import ElasticSearch

from mock import patch


class ElasticSearchTest(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.es = ElasticSearch("http://url.com", "index", "app")

    @patch("requests.post")
    def test_cpu_max(self, post_mock):
        self.es.cpu_max()
        post_mock.assert_called_with(self.es.url, data=self.es.query(key="cpu_max"))

    @patch("requests.post")
    def test_mem_max(self, post_mock):
        self.es.mem_max()
        post_mock.assert_called_with(self.es.url, data=self.es.query(key="mem_max"))

    @patch("requests.post")
    def test_units(self, post_mock):
        self.es.units()
        post_mock.assert_called_with(self.es.url, data=self.es.query(key="cpu_max"))

    @patch("requests.post")
    def test_requests_min(self, post_mock):
        self.es.requests_min()
        post_mock.assert_called_with(self.es.url, data=self.es.query(key="response_time"))

    @patch("requests.post")
    def test_response_time(self, post_mock):
        self.es.response_time()
        post_mock.assert_called_with(self.es.url, data=self.es.query(key="response_time"))

    @patch("requests.post")
    def test_connections(self, post_mock):
        self.es.connections()
        post_mock.assert_called_with(self.es.url, data=self.es.query(key="connection"))

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
                "range": {
                    "buckets": [
                        {
                            "key": "2015-07-21T19:35:00.000Z-2015-07-21T19:37:05.388Z",
                            "from": 1437507300000,
                            "from_as_string": "2015-07-21T19:35:00.000Z",
                            "to": 1437507425388,
                            "to_as_string": "2015-07-21T19:37:05.388Z",
                            "doc_count": 18,
                            "date": {
                                "buckets": [
                                    {
                                        "key_as_string": "2015-07-21T19:35:00.000Z",
                                        "key": 1437507300000,
                                        "doc_count": 9,
                                        "min": {
                                            "value": 97517568
                                        },
                                        "max": {
                                            "value": 97517568
                                        },
                                        "avg": {
                                            "value": 97517568
                                        }
                                    },
                                    {
                                        "key_as_string": "2015-07-21T19:36:00.000Z",
                                        "key": 1437507360000,
                                        "doc_count": 9,
                                        "min": {
                                            "value": 97517568
                                        },
                                        "max": {
                                            "value": 97517568
                                        },
                                        "avg": {
                                            "value": 97517568
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        }
        expected = {
            "data": [
                {
                    "x": 1437507300000,
                    "max": "93.00",
                    "min": "93.00",
                    "avg": "93.00"
                },
                {
                    "x": 1437507360000,
                    "max": "93.00",
                    "min": "93.00",
                    "avg": "93.00"
                }
            ],
            "min": "93.00",
            "max": "93.00"
        }
        d = self.es.process(data)
        self.assertDictEqual(d, expected)
