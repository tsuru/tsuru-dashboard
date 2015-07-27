from django.conf import settings

import requests
import json


class MetricNotEnabled(Exception):
    pass


def get_backend(app):
    if "envs" in app and "ELASTICSEARCH_HOST" in app["envs"]:
        return ElasticSearch(app["envs"]["ELASTICSEARCH_HOST"], ".measure-tsuru-*", app["name"])

    response = requests.get("{}/apps/tsuru-dashboard/metric/envs".format(
        settings.TSURU_HOST,
    ))
    if response.status_code == 200:
        data = response.json()
        if "METRICS_ELASTICSEARCH_HOST" in data:
            return ElasticSearch(data["METRICS_ELASTICSEARCH_HOST"], ".measure-tsuru-*", app["name"])
    raise MetricNotEnabled


class ElasticSearch(object):
    def __init__(self, url, index, app):
        self.index = index
        self.app = app
        self.url = url

    def post(self, data, metric):
        url = "{}/.measure-tsuru-*/{}/_search".format(self.url, metric)
        data = requests.post(url, data=json.dumps(data))
        return data.json()

    def process(self, data, formatter=None):
        d = []
        min_value = None
        max_value = 0

        for bucket in data["aggregations"]["range"]["buckets"][0]["date"]["buckets"]:
            bucket_max = bucket["max"]["value"]
            bucket_min = bucket["min"]["value"]
            bucket_avg = bucket["avg"]["value"]

            if min_value is None:
                min_value = bucket_min

            if bucket_min < min_value:
                min_value = bucket_min

            if bucket_max > max_value:
                max_value = bucket_max

            d.append({
                "x": bucket["key"],
                "max": bucket_max,
                "min": bucket_min,
                "avg": bucket_avg,
            })

        return {
            "data": d,
            "min": min_value,
            "max": max_value,
        }

    def cpu_max(self):
        query = self.query()
        response = self.post(query, "cpu_max")
        process = self.process(response)
        return process

    def mem_max(self):
        return self.process(self.post(self.query(), "mem_max"))

    def units(self):
        aggregation = {"units": {"cardinality": {"field": "host"}}}
        return self.units_process(self.post(self.query(aggregation=aggregation), "cpu_max"))

    def units_process(self, data, formatter=None):
        d = []
        min_value = None
        max_value = 0

        for bucket in data["aggregations"]["range"]["buckets"][0]["date"]["buckets"]:
            value = bucket["units"]["value"]

            if min_value is None:
                min_value = value

            if value < min_value:
                min_value = value

            if value > max_value:
                max_value = value

            d.append({
                "x": bucket["key"],
                "units": value,
            })

        return {
            "data": d,
            "min": min_value,
            "max": max_value,
        }

    def requests_min(self):
        aggregation = {"sum": {"sum": {"field": "count"}}}
        return self.requests_min_process(self.post(self.query(aggregation=aggregation), "response_time"))

    def requests_min_process(self, data, formatter=None):
        d = []
        min_value = None
        max_value = 0

        for bucket in data["aggregations"]["range"]["buckets"][0]["date"]["buckets"]:
            value = bucket["sum"]["value"]

            if min_value is None:
                min_value = value

            if value < min_value:
                min_value = value

            if value > max_value:
                max_value = value

            d.append({
                "x": bucket["key"],
                "sum": value,
            })

        return {
            "data": d,
            "min": min_value,
            "max": max_value,
        }

    def response_time(self):
        return self.process(self.post(self.query(), "response_time"))

    def connections(self):
        aggregation = {"connection": {"terms": {"field": "connection.raw"}}}
        return self.connections_process(self.post(self.query(aggregation=aggregation), "connection"))

    def connections_process(self, data, formatter=None):
        d = []
        min_value = 0
        max_value = 0

        for bucket in data["aggregations"]["range"]["buckets"][0]["date"]["buckets"]:
            obj = {}
            obj["x"] = bucket["key"]

            for doc in bucket["connection"]["buckets"]:
                size = doc["doc_count"]
                conn = doc["key"]

                if size < min_value:
                    min_value = size

                if size > max_value:
                    max_value = size

                obj[conn] = size

            d.append(obj)

        return {
            "data": d,
            "min": min_value,
            "max": max_value,
        }

    def query(self, date_range="1h/h", interval="1m", aggregation=None):
        query_filter = {
            "filtered": {
                "filter": {
                    "term": {
                        "app.raw": self.app,
                    }
                }
            }
        }
        if not aggregation:
            aggregation = {
                "max": {"max": {"field": "value"}},
                "min": {"min": {"field": "value"}},
                "avg": {"avg": {"field": "value"}}
            }
        return {
            "query": query_filter,
            "size": 0,
            "aggs": {
                "range": {
                    "date_range": {
                        "field": "@timestamp",
                        "ranges": [{
                            "from": "now-" + date_range,
                            "to": "now"
                        }]
                    },
                    "aggs": {
                        "date": {
                            "date_histogram": {
                                "field": "@timestamp",
                                "interval": interval
                            },
                            "aggs": aggregation,
                        }
                    }
                }
            }
        }
