import requests


class ElasticSearch(object):
    def __init__(self, url, index, app):
        self.index = index
        self.app = app
        self.url = url

    def post(self, data):
        data = requests.post(self.url, data=data)
        return data.json()

    def cpu_max(self):
        return self.post(self.query(key="cpu_max"))

    def mem_max(self):
        return self.post(self.query(key="mem_max"))

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
