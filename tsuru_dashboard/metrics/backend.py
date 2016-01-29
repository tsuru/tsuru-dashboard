from tsuru_dashboard import settings

import requests
import json
import datetime


class MetricNotEnabled(Exception):
    pass


def get_backend(app, token, date_range=None, process_name=None):
    headers = {'authorization': token}
    url = "{}/apps/{}/metric/envs".format(settings.TSURU_HOST, app["name"])
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "METRICS_ELASTICSEARCH_HOST" in data:
            return ElasticSearch(
                url=data["METRICS_ELASTICSEARCH_HOST"],
                app=app["name"],
                process_name=process_name,
                date_range=date_range
            )

    if "envs" in app and "ELASTICSEARCH_HOST" in app["envs"]:
        return ElasticSearch(
            url=app["envs"]["ELASTICSEARCH_HOST"],
            app=app["name"],
            process_name=process_name,
            date_range=date_range
        )

    raise MetricNotEnabled


NET_AGGREGATION = {
    "units": {
        "terms": {
            "field": "host"
        },
        "aggs": {
            "delta": {
                "scripted_metric": {
                    "init_script": """
_agg['max'] = [ts: 0, val: null]
_agg['min'] = [ts: 0, val: null]
""",
                    "map_script": """
ts = doc['@timestamp'][0]
val = doc['value'][0]
if (ts > _agg.max.ts) {
    _agg.max.ts = ts
    _agg.max.val = val
}
if (_agg.min.ts == 0 || ts < _agg.min.ts) {
    _agg.min.ts = ts
    _agg.min.val = val
}
""",
                    "reduce_script": """
max = null
min = null
for (a in _aggs) {
    if (max == null || a.max.ts > max.ts) {
        max = a.max
    }
    if (min == null || a.min.ts < min.ts) {
        min = a.min
    }
}
dt = max.ts - min.ts
if (dt > 0) {
    return ((max.val - min.val)/1024)/(dt/1000)
} else {
    return 0
}
"""
                }
            }
        }
    }
}


class ElasticSearch(object):
    def __init__(self, url, app, process_name=None, date_range="1h"):
        if date_range == "1h":
            self.index = ".measure-tsuru-{}".format(datetime.datetime.utcnow().strftime("%Y.%m.%d"))
        else:
            self.index = ".measure-tsuru-{}.*".format(datetime.datetime.utcnow().strftime("%Y"))
        self.app = app
        self.url = url
        self.process_name = process_name
        self.date_range = date_range

    def post(self, data, metric):
        url = "{}/{}/{}/_search".format(self.url, self.index, metric)
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

        if "aggregations" in data and len(data["aggregations"]["date"]["buckets"]) > 0:
            for bucket in data["aggregations"]["date"]["buckets"]:
                bucket_max = formatter(bucket["stats"]["max"])
                bucket_min = formatter(bucket["stats"]["min"])
                bucket_avg = formatter(bucket["stats"]["avg"])

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

    def cpu_max(self, interval=None):
        query = self.query(interval=interval)
        response = self.post(query, "cpu_max")
        process = self.process(response)
        return process

    def mem_max(self, interval=None):
        query = self.query(interval=interval)
        return self.process(self.post(query, "mem_max"), formatter=lambda x: x / (1024 * 1024))

    def swap(self, interval=None):
        query = self.query(interval=interval)
        return self.process(self.post(query, "swap"), formatter=lambda x: x / (1024 * 1024))

    def netrx(self, interval=None):
        return self.net_metric("netrx", interval)

    def nettx(self, interval=None):
        return self.net_metric("nettx", interval)

    def net_metric(self, kind, interval=None):
        query = self.query(interval=interval, aggregation=NET_AGGREGATION)
        data = self.post(query, kind)
        return self.net_process(data)

    def net_process(self, data):
        result = {}
        min_value = None
        max_value = 0

        if "aggregations" in data and len(data["aggregations"]["date"]["buckets"]) > 0:
            for bucket in data["aggregations"]["date"]["buckets"]:
                value = 0
                for in_bucket in bucket["units"]["buckets"]:
                    value += in_bucket["delta"]["value"]

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

    def units(self, interval=None):
        aggregation = {"units": {"cardinality": {"field": "host"}}}
        query = self.query(interval=interval, aggregation=aggregation)
        return self.units_process(self.post(query, "cpu_max"))

    def units_process(self, data, formatter=None):
        result = {}
        min_value = None
        max_value = 0

        if "aggregations" in data and len(data["aggregations"]["date"]["buckets"]) > 0:
            for bucket in data["aggregations"]["date"]["buckets"]:
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

    def requests_min(self, interval=None):
        aggregation = {"sum": {"sum": {"field": "count"}}}
        query = self.query(interval=interval, aggregation=aggregation)
        return self.requests_min_process(self.post(query, "response_time"))

    def requests_min_process(self, data, formatter=None):
        result = {}
        min_value = None
        max_value = 0

        if "aggregations" in data and len(data["aggregations"]["date"]["buckets"]) > 0:
            for bucket in data["aggregations"]["date"]["buckets"]:
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

    def response_time(self, interval=None):
        query = self.query(interval=interval)
        return self.process(self.post(query, "response_time"))

    def connections(self, interval=None):
        aggregation = {"connection": {"terms": {"field": "connection.raw"}}}
        query = self.query(interval=interval, aggregation=aggregation)
        return self.connections_process(self.post(query, "connection"))

    def connections_process(self, data, formatter=None):
        result = {}
        min_value = 0
        max_value = 0

        if "aggregations" in data and len(data["aggregations"]["date"]["buckets"]) > 0:
            for bucket in data["aggregations"]["date"]["buckets"]:
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

    def query(self, interval=None, aggregation=None):
        if not interval:
            interval = "1m"

        f = {
            "bool": {
                "must": [
                    {
                        "term": {
                            "app": self.app,
                            "app.raw": self.app,
                        }
                    },
                    {
                        "range": {
                            "@timestamp": {
                                "gte": "now-" + self.date_range,
                                "lt": "now"
                            }
                        },
                    }
                ],
            }
        }

        if self.process_name:
            p = {
                "term": {
                    "process.raw": self.process_name,
                    "process": self.process_name,
                },
            }
            f["bool"]["must"].append(p)

        query_filter = {
            "filtered": {
                "filter": f
            }
        }
        if not aggregation:
            aggregation = {"stats": {"stats": {"field": "value"}}}
        return {
            "query": query_filter,
            "size": 0,
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
