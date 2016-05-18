from tsuru_dashboard import settings

import requests
import json
import datetime
import re


NET_AGGREGATION = {
    "units": {
        "terms": {
            "field": "host.raw"
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


class ElasticSearchFilter(object):
    def query(self):
        return {
            "filtered": {
                "filter": self.filter
            }
        }

    def term_filter(self, field, value):
        return {"term": {field: value}}

    def terms_filter(self, field, values):
        if(type(values) is not list):
            values = [values]
        return {"terms": {field: values}}

    def timestamp_filter(self, date_range):
        if date_range is None:
            date_range = "1h"
        return {"range": {"@timestamp": {"gte": "now-" + date_range, "lt": "now"}}}

    def metric_filter(self, *filters):
        bool_filter = {
            "bool": {
                "must": [
                    self.timestamp_filter(self.date_range)
                ]
            }
        }
        bool_filter["bool"]["must"].append({"bool": {"should": list(filters)}})

        return bool_filter


class NodeFilter(ElasticSearchFilter):
    def __init__(self, node, date_range=None):
        self.date_range = date_range
        self.filter = self.node_filter(node)

    def node_filter(self, node):
        return self.metric_filter(self.terms_filter("addr.raw", node))


class ComponentFilter(ElasticSearchFilter):
    def __init__(self, component, date_range=None):
        self.date_range = date_range
        self.filter = self.component_filter(component)

    def component_filter(self, component):
        return self.metric_filter(
            self.term_filter("container", component), self.term_filter("container.raw", component))


class AppFilter(ElasticSearchFilter):
    def __init__(self, app, process_name=None, date_range=None):
        self.date_range = date_range
        self.filter = self.app_filter(app, process_name)

    def app_filter(self, app, process_name):
        f = self.metric_filter(self.term_filter("app", app), self.term_filter("app.raw", app))

        if process_name:
            p = {
                "bool": {
                    "should": [
                        self.term_filter("process", process_name),
                        self.term_filter("process.raw", process_name)
                    ]
                }
            }
            f["bool"]["must"].append(p)
        return f


class ElasticSearch(object):
    def __init__(self, url, query, date_range="1h"):
        if date_range is None:
            date_range = "1h"
        if date_range == "1h":
            self.index = ".measure-tsuru-{}".format(datetime.datetime.utcnow().strftime("%Y.%m.%d"))
        else:
            self.index = ".measure-tsuru-{}.*".format(datetime.datetime.utcnow().strftime("%Y"))
        self.url = url
        self.filtered_query = query
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

        def processor(result, bucket):
            bucket_max = formatter(bucket["stats"]["max"])
            bucket_min = formatter(bucket["stats"]["min"])
            bucket_avg = formatter(bucket["stats"]["avg"])
            if not result:
                result = {
                    "max": [],
                    "min": [],
                    "avg": [],
                }
            result["max"].append([bucket["key"], bucket_max])
            result["min"].append([bucket["key"], bucket_min])
            result["avg"].append([bucket["key"], bucket_avg])
            return result, bucket_min, bucket_max

        return self.base_process(data, processor)

    def cpu_max(self, interval=None):
        query = self.query(interval=interval)
        query["query"]["filtered"]["filter"]["bool"]["must"].append(
            {"range": {"value": {"lt": 500}}}
        )
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
        return self.base_process(self.post(query, kind), self.net_process)

    def net_process(self, result, bucket):
        value = 0
        for in_bucket in bucket["units"]["buckets"]:
            value += in_bucket["delta"]["value"]
        if not result:
            result["requests"] = []
        result["requests"].append([bucket["key"], value])
        return result, value, value

    def units(self, interval=None):
        aggregation = {"units": {"cardinality": {"field": "host.raw"}}}
        query = self.query(interval=interval, aggregation=aggregation)
        return self.base_process(self.post(query, "cpu_max"), self.units_process)

    def units_process(self, result, bucket):
        value = bucket["units"]["value"]
        if not result:
            result["units"] = []
        result["units"].append([bucket["key"], value])
        return result, value, value

    def requests_min(self, interval=None):
        aggregation = {"sum": {"sum": {"field": "count"}}}
        query = self.query(interval=interval, aggregation=aggregation)
        return self.base_process(self.post(query, "response_time"), self.requests_min_process)

    def requests_min_process(self, result, bucket):
        value = bucket["sum"]["value"]
        if not result:
            result["requests"] = []
        result["requests"].append([bucket["key"], value])
        return result, value, value

    def response_time(self, interval=None):
        aggregation = {
            "stats": {"stats": {"field": "value"}},
            "percentiles": {"percentiles": {"field": "value"}}
        }
        query = self.query(interval=interval, aggregation=aggregation)
        return self.base_process(self.post(query, "response_time"), self.response_time_process)

    def response_time_process(self, result, bucket):
        bucket_max = bucket["stats"]["max"]
        bucket_min = bucket["stats"]["min"]
        bucket_avg = bucket["stats"]["avg"]
        if not result:
            result = {
                "max": [],
                "min": [],
                "avg": [],
                "p95": [],
                "p99": [],
            }
        result["max"].append([bucket["key"], bucket_max])
        result["min"].append([bucket["key"], bucket_min])
        result["avg"].append([bucket["key"], bucket_avg])
        result["p95"].append([bucket["key"], bucket["percentiles"]["values"]["95.0"]])
        result["p99"].append([bucket["key"], bucket["percentiles"]["values"]["99.0"]])
        return result, bucket_min, bucket_max

    def top_slow(self, interval=None):
        aggregation = {
            "top": {
                "terms": {
                    "script": "doc['method'].value +'U'+doc['path.raw'].value +'U'+doc['status_code'].value"
                },
                "aggs": {"max": {"max": {"field": "value"}}}
            }
        }
        query = self.query(interval=interval, aggregation=aggregation)
        return self.base_process(self.post(query, "response_time"), self.top_slow_process)

    def top_slow_process(self, result, bucket):
        max_response = 0
        for b in bucket["top"]["buckets"]:
            response_time = b["max"]["value"]
            if response_time > max_response:
                max_response = response_time
            r = r'(?P<method>\w+)U(?P<path>.*)U(?P<status_code>\d{3})'
            info = re.search(r, b["key"])
            path = info.groupdict()['path']
            status_code = info.groupdict()['status_code']
            method = info.groupdict()['method']

            if path not in result:
                result[path] = []

            result[path].append([bucket["key"], response_time, status_code, method])

        return result, 0, max_response

    def http_methods(self, interval=None):
        aggregation = {"method": {"terms": {"field": "method"}}}
        query = self.query(interval=interval, aggregation=aggregation)
        return self.base_process(self.post(query, "response_time"), self.http_methods_process)

    def http_methods_process(self, result, bucket):
        max_value = 0
        min_value = 0

        for doc in bucket["method"]["buckets"]:
            value = doc["doc_count"]
            method = doc["key"]

            if method not in result:
                result[method] = []

            if value < min_value:
                min_value = value

            if value > max_value:
                max_value = value

            result[method].append([bucket["key"], value])
        return result, min_value, max_value

    def status_code(self, interval=None):
        aggregation = {"status_code": {"terms": {"field": "status_code"}}}
        query = self.query(interval=interval, aggregation=aggregation)
        return self.base_process(self.post(query, "response_time"), self.status_code_process)

    def status_code_process(self, result, bucket):
        max_value = 0
        min_value = 0

        for doc in bucket["status_code"]["buckets"]:
            value = doc["doc_count"]
            code = doc["key"]

            if code not in result:
                result[code] = []

            if value < min_value:
                min_value = value

            if value > max_value:
                max_value = value

            result[code].append([bucket["key"], value])
        return result, min_value, max_value

    def connections(self, interval=None):
        aggregation = {
            "connection": {
                "terms": {"field": "connection.raw"}
            }
        }
        query = self.query(interval=interval, aggregation=aggregation)
        return self.base_process(self.post(query, "connection"), self.connections_process)

    def connections_process(self, result, bucket):
        min_value = 0
        max_value = 0
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
        return result, min_value, max_value

    def base_process(self, data, processor):
        result = {}
        min_value = None
        max_value = 0

        if "aggregations" in data and len(data["aggregations"]["date"]["buckets"]) > 0:
            for bucket in data["aggregations"]["date"]["buckets"]:
                result, min_v, max_v = processor(result, bucket)
                if min_value is None or min_v < min_value:
                    min_value = min_v
                if max_v > max_value:
                    max_value = max_v

        return {
            "data": result,
            "min": min_value or 0,
            "max": max_value + 1,
        }

    def query(self, interval=None, aggregation=None):
        if not interval:
            interval = "1m"

        if not aggregation:
            aggregation = {"stats": {"stats": {"field": "value"}}}
        return {
            "query": self.filtered_query,
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


class MetricNotEnabled(Exception):
    pass


class AppBackend(ElasticSearch):
    def __init__(self, app, token, process_name=None, date_range=None):
        headers = {'authorization': token}
        url = "{}/apps/{}/metric/envs".format(settings.TSURU_HOST, app["name"])
        response = requests.get(url, headers=headers)

        es_query = AppFilter(app=app["name"], process_name=process_name, date_range=date_range).query()

        if response.status_code == 200:
            data = response.json()
            if "METRICS_ELASTICSEARCH_HOST" in data:
                return super(AppBackend, self).__init__(
                    url=data["METRICS_ELASTICSEARCH_HOST"],
                    query=es_query,
                    date_range=date_range
                )

        if "envs" in app and "ELASTICSEARCH_HOST" in app["envs"]:
            return super(AppBackend, self).__init__(
                url=app["envs"]["ELASTICSEARCH_HOST"],
                query=es_query,
                date_range=date_range
            )

        raise MetricNotEnabled


class TsuruMetricsBackend(ElasticSearch):
    def __init__(self, filter, date_range=None):
        return super(TsuruMetricsBackend, self).__init__(
            url=settings.ELASTICSEARCH_HOST, query=filter.query(), date_range=date_range)


class NodeMetricsBackend(TsuruMetricsBackend):
    def __init__(self, addr, date_range=None):
        filter = NodeFilter(node=addr, date_range=date_range)
        return super(NodeMetricsBackend, self).__init__(filter=filter, date_range=date_range)

    def multi_index_avg(self, result, bucket, formatter=None):
        if formatter is None:
            def formatter(x):
                return x
        for b in bucket["stats"]["buckets"]:
            result[b["key"].split('_')[-1]].append([bucket["key"], formatter(b["stats"]["avg"])])
        return result, None, None

    def load_process(self, result, bucket):
        if not result:
            result = {
                "load1": [],
                "load5": [],
                "load15": [],
            }
        return self.multi_index_avg(result, bucket)

    def cpu_max_process(self, result, bucket):
        if not result:
            result = {
                "user": [],
                "sys": [],
                "wait": [],
            }
        return self.multi_index_avg(result, bucket, formatter=lambda x: x * 100)

    def disk_process(self, result, bucket):
        if not result:
            result = {
                "used": [],
                "total": []
            }
        return self.multi_index_avg(result, bucket, formatter=lambda x: x / (1024 * 1024))

    def per_type_agg(self):
        return {
            "stats": {
                "terms": {"field": "_type"},
                "aggs": {"stats": {"stats": {"field": "value"}}}
            }
        }

    def load(self, interval=None):
        query = self.query(interval=interval, aggregation=self.per_type_agg())
        return self.base_process(self.post(query, "host_load1,host_load5,host_load15"), self.load_process)

    def cpu_max(self, interval=None):
        query = self.query(interval=interval, aggregation=self.per_type_agg())
        process = self.base_process(self.post(
            query, "host_cpu_user,host_cpu_sys,host_cpu_wait"), self.cpu_max_process)
        return process

    def mem_max(self, interval=None):
        query = self.query(interval=interval)
        return self.process(self.post(query, "host_mem_used"), formatter=lambda x: x / (1024 * 1024))

    def netrx(self, interval=None):
        return self.net_metric("host_netrx", interval)

    def nettx(self, interval=None):
        return self.net_metric("host_nettx", interval)

    def swap(self, interval=None):
        query = self.query(interval=interval, aggregation=self.per_type_agg())
        return self.base_process(self.post(query, "host_swap_used,host_swap_total"), self.disk_process)

    def disk(self, interval=None):
        query = self.query(interval=interval, aggregation=self.per_type_agg())
        return self.base_process(self.post(query, "host_disk_used,host_disk_total"), self.disk_process)


class NodesMetricsBackend(TsuruMetricsBackend):
    def __init__(self, addrs, date_range=None):
        self.addrs = addrs
        filter = NodeFilter(node=addrs, date_range=date_range)
        return super(NodesMetricsBackend, self).__init__(filter=filter, date_range=date_range)

    def process(self, data, formatter=None, processor=None):
        if formatter is None:
            def default_formatter(x):
                return x
            formatter = default_formatter
        if processor is None:
            def default_processor(result, bucket):
                if not result:
                    result = {}
                    for addr in self.addrs:
                        result[addr] = []

                for b in bucket["addrs"]["buckets"]:
                    result[b["key"]].append([bucket["key"], formatter(b["avg"]["value"])])
                return result, None, None
            processor = default_processor
        return self.base_process(data=data, processor=processor)

    def per_addr_agg(self, aggs=None):
        if aggs is None:
            aggs = {"avg": {"avg": {"field": "value"}}}
        return {
            "addrs": {
                "terms": {
                    "field": "addr.raw",
                    "include": '|'.join(self.addrs),
                    "size": len(self.addrs)
                },
                "aggs": aggs
            }
        }

    def mem_max(self, interval=None):
        query = self.query(interval=interval, aggregation=self.per_addr_agg())
        return self.process(self.post(query, "host_mem_used"), formatter=lambda x: x / (1024 * 1024))

    def cpu_max(self, interval=None):
        query = self.query(interval=interval, aggregation=self.per_addr_agg())
        return self.process(self.post(query, "host_cpu_busy"), formatter=lambda x: x * 100)

    def cpu_wait(self, interval=None):
        query = self.query(interval=interval, aggregation=self.per_addr_agg())
        return self.process(self.post(query, "host_cpu_wait"), formatter=lambda x: x * 100)

    def swap(self, interval=None):
        query = self.query(interval=interval, aggregation=self.per_addr_agg())
        return self.process(self.post(query, "host_swap_used"), formatter=lambda x: x / (1024 * 1024))

    def disk(self, interval=None):
        query = self.query(interval=interval, aggregation=self.per_addr_agg())
        return self.process(self.post(query, "host_disk_used"), formatter=lambda x: x / (1024 * 1024))

    def netrx(self, interval=None):
        query = self.query(interval=interval, aggregation=self.per_addr_agg(
            aggs=NET_AGGREGATION["units"]["aggs"]))
        return self.process(self.post(query, "host_netrx"), processor=self.net_processor)

    def nettx(self, interval=None):
        query = self.query(interval=interval, aggregation=self.per_addr_agg(
            aggs=NET_AGGREGATION["units"]["aggs"]))
        return self.process(self.post(query, "host_nettx"), processor=self.net_processor)

    def load1(self, interval=None):
        return self.load(mins=1, interval=interval)

    def load5(self, interval=None):
        return self.load(mins=5, interval=interval)

    def load15(self, interval=None):
        return self.load(mins=15, interval=interval)

    def load(self, mins, interval=None):
        query = self.query(interval=interval, aggregation=self.per_addr_agg())
        return self.process(self.post(query, "host_load" + str(mins)))

    def net_processor(self, result, bucket):
        if not result:
            result = {}
            for addr in self.addrs:
                result[addr] = []
        for b in bucket["addrs"]["buckets"]:
            result[b["key"]].append([bucket["key"], b["delta"]["value"]])
        return result, None, None
