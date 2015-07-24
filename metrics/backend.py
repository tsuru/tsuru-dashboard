from django.conf import settings

import requests


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

    def post(self, data):
        url = "{}/.measure-tsuru-*/{}/_search".format(self.url, data["type"])
        data = requests.post(url, data=data)
        return data.json()

    def process(self, data):
        d = []
        min_value = None
        max_value = 0

        for bucket in data["aggregations"]["range"]["buckets"][0]["date"]["buckets"]:
            bucket_max = bucket["max"]["value"] / (1024 * 1024)
            bucket_min = bucket["min"]["value"] / (1024 * 1024)
            bucket_avg = bucket["avg"]["value"] / (1024 * 1024)

            if min_value is None:
                min_value = bucket_min

            if bucket_min < min_value:
                min_value = bucket_min

            if bucket_max > max_value:
                max_value = bucket_max

            d.append({
                "x": bucket["key"],
                "max": "{0:.2f}".format(bucket_max),
                "min": "{0:.2f}".format(bucket_min),
                "avg": "{0:.2f}".format(bucket_avg),
            })

        return {
            "data": d,
            "min": "{0:.2f}".format(min_value),
            "max": "{0:.2f}".format(max_value),
        }

    def cpu_max(self):
        query = self.query(key="cpu_max")
        response = self.post(query)
        process = self.process(response)
        return process

    def mem_max(self):
        return self.process(self.post(self.query(key="mem_max")))

    def units(self):
        return self.post(self.query(key="cpu_max"))

    def requests_min(self):
        return self.post(self.query(key="response_time"))

    def response_time(self):
        return self.post(self.query(key="response_time"))

    def connections(self):
        return self.post(self.query(key="connection"))

    def query(self, key, date_range="", interval="1m", aggregation=None):
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
            "index": self.index,
            "type": key,
            "body": {
                "query": query_filter,
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
        }
