from tsuru_dashboard import settings
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
        headers = {'authorization': token}
        url = "{}/apps/{}/metric/envs".format(settings.TSURU_HOST, app["name"])
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if "METRICS_PROMETHEUS_HOST" in data:
                return super(AppBackend, self).__init__(
                    url=data["METRICS_PROMETHEUS_HOST"],
                    query='name=~"%s.*"' % app["name"]
                )

        raise base.MetricNotEnabled
