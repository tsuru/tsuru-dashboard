from tsuru_dashboard.metrics.backends import base

import requests


class Prometheus(object):
    def __init__(self, url, query):
        self.url = url
        self.query = query

    def mem_max(self, interval=None):
        url = self.url
        url += "/api/v1/query_range?"
        url += 'query=avg(container_memory_usage_bytes{%s})/1024/1024&' % self.query
        url += "start=1473209927.011&end=1473213527.011&step=14"
        result = requests.get(url)
        return result.json()


class AppBackend(Prometheus):
    def __init__(self, app, token, process_name=None, date_range=None):
        envs = base.get_envs_from_api(app, token)

        if envs and "METRICS_PROMETHEUS_HOST" in envs:
            return super(AppBackend, self).__init__(
                url=envs["METRICS_PROMETHEUS_HOST"],
                query='name=~"%s.*"' % app["name"]
            )

        raise base.MetricNotEnabled
