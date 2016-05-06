from django.test import TestCase
from tsuru_dashboard.metrics.backend import AppFilter, ComponentFilter


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
