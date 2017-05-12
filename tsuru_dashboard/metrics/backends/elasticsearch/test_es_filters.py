from django.test import TestCase
from tsuru_dashboard.metrics.backends.elasticsearch import AppFilter, ComponentFilter, NodeFilter


class ElasticSearchFilterTest(TestCase):
    def test_app_filters(self):
        expected_filter = {
            "bool": {
                "must": [
                    {
                        "range": {
                            "@timestamp": {
                                "gte": "now-1h",
                                "lt": "now"
                            }
                        }
                    },
                    {
                        "term": {"app.keyword": "app_name"}
                    },
                    {
                        "term": {"process.keyword": "process_name"}
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
                        "range": {
                            "@timestamp": {
                                "gte": "now-1h",
                                "lt": "now"
                            }
                        }
                    },
                    {
                        "term": {"container.keyword": "comp_name"}
                    },
                ]
            }
        }
        filter = ComponentFilter(component="comp_name").filter
        self.assertDictEqual(filter, expected_filter)

    def test_node_filters(self):
        expected_filter = {
            "bool": {
                "must": [
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
                                {"terms": {"addr.keyword": ["127.0.0.1"]}},
                            ]
                        },
                    },
                ]
            }
        }
        filter = NodeFilter(node="127.0.0.1").filter
        self.assertDictEqual(filter, expected_filter)
