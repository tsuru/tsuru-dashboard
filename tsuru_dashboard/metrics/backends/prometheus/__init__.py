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
        query = "query=avg(container_memory_usage_bytes{%s})/1024/1024&" % self.query
        return self.get_metrics(query)


class AppBackend(Prometheus):
    def __init__(self, app, url, process_name=None, date_range=None):
        return super(AppBackend, self).__init__(
            url=url,
            query='name=~"%s.*"' % app["name"]
        )
