from tsuru_dashboard import settings

import requests
import json


class MetricNotEnabled(Exception):
    pass


def metrics_from_api(app):
    for unit in app.get("units", []):
        if "ProcessName" in unit:
            return True
    return False


def get_backend(app, token):
    if metrics_from_api(app):
        headers = {'authorization': token}
        url = "{}/apps/{}/metric/envs".format(settings.TSURU_HOST, app["name"])
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if "METRICS_ELASTICSEARCH_HOST" in data:
                return ElasticSearch(data["METRICS_ELASTICSEARCH_HOST"], ".measure-tsuru-*", app["name"])
    else:
        if "envs" in app and "ELASTICSEARCH_HOST" in app["envs"]:
            return ElasticSearch(app["envs"]["ELASTICSEARCH_HOST"], ".measure-tsuru-*", app["name"])

    raise MetricNotEnabled


class ElasticSearch(object):
    def __init__(self, url, index, app, process_name=None):
        self.index = index
        self.app = app
        self.url = url

    def post(self, data, metric):
        url = "{}/.measure-tsuru-*/{}/_search".format(self.url, metric)
        result = requests.post(url, data=json.dumps(data))
        return result.json()

    def process(self, data, formatter=None):
        if not formatter:
            def default_formatter(x):
                return x
            formatter = default_formatter

        result = {}
        min_value = None
        max_value = 0

        if "aggregations" in data and data["aggregations"]["range"]["buckets"][0]["doc_count"] > 0:
            for bucket in data["aggregations"]["range"]["buckets"][0]["date"]["buckets"]:
                bucket_max = formatter(bucket["max"]["value"])
                bucket_min = formatter(bucket["min"]["value"])
                bucket_avg = formatter(bucket["avg"]["value"])

                if min_value is None:
                    min_value = bucket_min

                if bucket_min < min_value:
                    min_value = bucket_min

                if bucket_max > max_value:
                    max_value = bucket_max

                if not result:
                    result = {
                        "max": [],
                        "min": [],
                        "avg": [],
                    }
                result["max"].append([bucket["key"], "{0:.2f}".format(bucket_max)])
                result["min"].append([bucket["key"], "{0:.2f}".format(bucket_min)])
                result["avg"].append([bucket["key"], "{0:.2f}".format(bucket_avg)])

        return {
            "data": result,
            "min": "{0:.2f}".format(min_value or 0),
            "max": "{0:.2f}".format(max_value + 1),
        }

    def cpu_max(self, date_range=None, interval=None, process_name=None):
        query = self.query(date_range=date_range, interval=interval, process_name=process_name)
        response = self.post(query, "cpu_max")
        process = self.process(response)
        return process

    def mem_max(self, date_range=None, interval=None, process_name=None):
        query = self.query(date_range=date_range, interval=interval, process_name=process_name)
        return self.process(self.post(query, "mem_max"), formatter=lambda x: x / (1024 * 1024))

    def units(self, date_range=None, interval=None, process_name=None):
        aggregation = {"units": {"cardinality": {"field": "host"}}}
        query = self.query(date_range=date_range, interval=interval,
                           process_name=process_name, aggregation=aggregation)
        return self.units_process(self.post(query, "cpu_max"))

    def units_process(self, data, formatter=None):
        result = {}
        min_value = None
        max_value = 0

        if "aggregations" in data and data["aggregations"]["range"]["buckets"][0]["doc_count"] > 0:
            for bucket in data["aggregations"]["range"]["buckets"][0]["date"]["buckets"]:
                value = bucket["units"]["value"]

                if min_value is None:
                    min_value = value

                if value < min_value:
                    min_value = value

                if value > max_value:
                    max_value = value

                if not result:
                    result["units"] = []

                result["units"].append([bucket["key"], "{0:.2f}".format(value)])

        return {
            "data": result,
            "min": "{0:.2f}".format(min_value or 0),
            "max": "{0:.2f}".format(max_value),
        }

    def requests_min(self, date_range=None, interval=None, process_name=None):
        aggregation = {"sum": {"sum": {"field": "count"}}}
        query = self.query(date_range=date_range, interval=interval,
                           process_name=process_name, aggregation=aggregation)
        return self.requests_min_process(self.post(query, "response_time"))

    def requests_min_process(self, data, formatter=None):
        result = {}
        min_value = None
        max_value = 0

        if "aggregations" in data and data["aggregations"]["range"]["buckets"][0]["doc_count"] > 0:
            for bucket in data["aggregations"]["range"]["buckets"][0]["date"]["buckets"]:
                value = bucket["sum"]["value"]

                if min_value is None:
                    min_value = value

                if value < min_value:
                    min_value = value

                if value > max_value:
                    max_value = value

                if not result:
                    result["requests"] = []
                result["requests"].append([bucket["key"], value])

        return {
            "data": result,
            "min": min_value,
            "max": max_value,
        }

    def response_time(self, date_range=None, interval=None, process_name=None):
        query = self.query(date_range=date_range, interval=interval, process_name=process_name)
        return self.process(self.post(query, "response_time"))

    def connections(self, date_range=None, interval=None, process_name=None):
        aggregation = {"connection": {"terms": {"field": "connection.raw"}}}
        query = self.query(date_range=date_range, interval=interval,
                           process_name=process_name, aggregation=aggregation)
        return self.connections_process(self.post(query, "connection"))

    def connections_process(self, data, formatter=None):
        result = {}
        min_value = 0
        max_value = 0

        if "aggregations" in data and data["aggregations"]["range"]["buckets"][0]["doc_count"] > 0:
            for bucket in data["aggregations"]["range"]["buckets"][0]["date"]["buckets"]:
                for doc in bucket["connection"]["buckets"]:
                    size = doc["doc_count"]
                    conn = doc["key"]
                    if conn not in result:
                        result[conn] = []

                    if size < min_value:
                        min_value = size

                    if size > max_value:
                        max_value = size

                    result[conn].append([bucket["key"], size])

        return {
            "data": result,
            "min": min_value,
            "max": max_value,
        }

    def query(self, date_range=None, interval=None, aggregation=None, process_name=None):
        if not date_range:
            date_range = "1h"

        if not interval:
            interval = "1m"

        f = {
            "bool": {
                "must": [{
                    "term": {
                        "app": self.app,
                        "app.raw": self.app,
                    }
                }],
            }
        }

        if process_name:
            p = {
                "term": {
                    "process.raw": process_name,
                    "process": process_name,
                },
            }
            f["bool"]["must"].append(p)

        query_filter = {
            "filtered": {
                "filter": f
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
