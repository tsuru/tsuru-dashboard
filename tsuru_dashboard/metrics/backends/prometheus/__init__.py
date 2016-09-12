import requests


class Prometheus(object):
    def __init__(self, url, query):
        self.url = url
        self.query = query

    def get_metrics(self, query):
        url = self.url
        url += "/api/v1/query_range?"
        url += 'query=avg(container_memory_usage_bytes{%s})/1024/1024&' % self.query
        url += "start=1473209927.011&end=1473213527.011&step=14"
        result = requests.get(url)
        return result.json()

    def mem_max(self, interval=None):
        data = {"min": 0, "max": 1024}
        query = "query=avg(container_memory_usage_bytes{%s})/1024/1024&" % self.query
        data["avg"] = self.get_metrics(query)

        query = "query=max(container_memory_usage_bytes{%s})/1024/1024&" % self.query
        data["max"] = self.get_metrics(query)

        query = "query=min(container_memory_usage_bytes{%s})/1024/1024&" % self.query
        data["min"] = self.get_metrics(query)
        return {"data": data}


class AppBackend(Prometheus):
    def __init__(self, app, url, process_name=None, date_range=None):
        return super(AppBackend, self).__init__(
            url=url,
            query='name=~"%s.*"' % app["name"]
        )
