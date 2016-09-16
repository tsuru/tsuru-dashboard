import requests

from datetime import datetime, timedelta
from time import mktime


class Prometheus(object):
    def __init__(self, url, query, date_range=None):
        self.url = url
        self.query = query
        self.date_range = date_range

    @property
    def delta(self):
        if not self.date_range:
            return {"hours": 1}

        if "h" in self.date_range:
            return {"hours": int(self.date_range.replace("h", ""))}

        if "d" in self.date_range:
            return {"days": int(self.date_range.replace("d", ""))}

        if "w" in self.date_range:
            return {"days": int(self.date_range.replace("w", ""))*7}

    @property
    def start(self):
        return self.end - timedelta(**self.delta)

    @property
    def end(self):
        return datetime.now()

    @property
    def resolution(self):
        return (self.end - self.start).total_seconds() / 250

    def get_metrics(self, query):
        url = self.url
        url += "/api/v1/query_range?"
        url += query
        url += "start={}".format(mktime(self.start.timetuple()))
        url += "&end={}".format(mktime(self.end.timetuple()))
        url += "&step={}".format(self.resolution)
        result = requests.get(url)
        return result.json()['data']['result'][0]['values']

    def mem_max(self, interval=None):
        data = {"min": 0, "max": 1024}
        query = "query=avg(container_memory_usage_bytes{%s})/1024/1024&" % self.query
        data["avg"] = self.get_metrics(query)

        query = "query=max(container_memory_usage_bytes{%s})/1024/1024&" % self.query
        data["max"] = self.get_metrics(query)

        query = "query=min(container_memory_usage_bytes{%s})/1024/1024&" % self.query
        data["min"] = self.get_metrics(query)
        return {"data": data}

    def cpu_max(self, interval=None):
        data = {"min": 0, "max": 100}
        query = "query=avg(rate(container_cpu_usage_seconds_total{%s}[2m]) * 100)&" % self.query
        data["avg"] = self.get_metrics(query)

        query = "query=max(rate(container_cpu_usage_seconds_total{%s}[2m]) * 100)&" % self.query
        data["max"] = self.get_metrics(query)

        query = "query=min(rate(container_cpu_usage_seconds_total{%s}[2m]) * 100)&" % self.query
        data["min"] = self.get_metrics(query)
        return {"data": data}

    def units(self, interval=None):
        data = {"min": 0, "max": 100}
        query = "query=max(count(rate(container_cpu_usage_seconds_total{%s}[2m])) by (slave))&" % self.query
        data["units"] = self.get_metrics(query)
        return {"data": data}


class AppBackend(Prometheus):
    def __init__(self, app, url, process_name=None, date_range=None):
        return super(AppBackend, self).__init__(
            url=url,
            query='name=~"%s.*"' % app["name"],
            date_range=date_range,
        )
