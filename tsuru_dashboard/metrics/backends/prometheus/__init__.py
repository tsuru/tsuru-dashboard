from time import mktime
from datetime import datetime, timedelta
import logging

import requests

from tsuru_dashboard.metrics.backends import base


logger = logging.getLogger(__name__)


class NoDataException(Exception):
    pass


class Prometheus(object):
    def __init__(self, url, date_range=None):
        self.url = url
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

    def default_processor(self, results):
        def toMs(x):
            if len(x) == 2:
                return [x[0]*1000, x[1]]
            return x
        return list(map(toMs, results))

    def get_metrics(self, query, processor=None):
        url = self.url
        url += "/api/v1/query_range"
        params = {
            'query': query,
            'start': mktime(self.start.timetuple()),
            'end': mktime(self.end.timetuple()),
            'step': self.resolution,
        }
        result = requests.get(url, params=params)
        response_data = result.json()
        logger.debug("Prometheus request: {}\nPrometheus response {}: {} - {}".format(
                     result.url, result.status_code, result.headers, response_data))

        if processor is None:
            result_data = response_data.get('data', {}).get('result', [])
            if len(result_data) == 0:
                raise NoDataException()
            response_data = result_data[0].get('values', [])
            processor = self.default_processor

        return processor(response_data)


class AppBackend(Prometheus):

    def __init__(self, app, url, process_name=None, date_range=None):
        query = 'container_label_app_name="%s"' % app["name"]
        if process_name is not None:
            query += ',container_label_app_process="%s"' % process_name
        self.app_name = app["name"]
        self.process_name = process_name
        self.app_metric_templates = [
            '{container_metric}{{container_name=~"{app_name}-{process_name}.*",{extra_query}}}',
            '{container_metric}{{container_name="POD",pod_name=~"{app_name}-{process_name}.*",{extra_query}}}',
            '{container_metric}{{container_label_app_name="{app_name}",container_label_app_process{process_name_op}"{process_name}",{extra_query}}}',
        ]
        return super(AppBackend, self).__init__(
            url=url,
            date_range=date_range,
        )

    def mem_max(self, interval=None):
        data = {"min": 0, "max": 1024}
        query = self.make_query(
            "container_memory_usage_bytes",
            "avg({})/1024/1024",
        )
        data["avg"] = self.get_metrics(query)

        query = self.make_query(
            "container_memory_usage_bytes",
            "max({})/1024/1024",
        )
        data["max"] = self.get_metrics(query)

        query = self.make_query(
            "container_memory_usage_bytes",
            "min({})/1024/1024",
        )
        data["min"] = self.get_metrics(query)
        return {"data": data}

    def cpu_max(self, interval=None):
        data = {"min": 0, "max": 100}
        query = self.make_query(
            "container_cpu_usage_seconds_total",
            "avg(sum(rate({}[2m])) by (name)) * 100",
        )
        data["avg"] = self.get_metrics(query)

        query = self.make_query(
            "container_cpu_usage_seconds_total",
            "max(sum(rate({}[2m])) by (name)) * 100",
        )
        data["max"] = self.get_metrics(query)

        query = self.make_query(
            "container_cpu_usage_seconds_total",
            "min(sum(rate({}[2m])) by (name)) * 100",
        )
        data["min"] = self.get_metrics(query)
        return {"data": data}

    def units(self, interval=None):
        data = {"min": 0, "max": 100}
        query = self.make_query(
            "container_memory_usage_bytes",
            "max(count(rate({}[2m])) by (slave))",
        )
        data["units"] = self.get_metrics(query)
        return {"data": data}

    def swap(self, interval=None):
        data = {"min": 0, "max": 1024}
        query = self.make_query(
            "container_memory_swap",
            "avg({})/1024/1024",
        )
        data["avg"] = self.get_metrics(query)

        query = self.make_query(
            "container_memory_swap",
            "max({})/1024/1024",
        )
        data["max"] = self.get_metrics(query)

        query = self.make_query(
            "container_memory_swap",
            "min({})/1024/1024",
        )
        data["min"] = self.get_metrics(query)
        return {"data": data}

    def netrx(self, interval=None):
        data = {"min": 0, "max": 100}
        query = self.make_query(
            "container_network_receive_bytes_total",
            "sum(rate({}[2m]))/1024",
        )
        data["netrx"] = self.get_metrics(query)
        return {"data": data}

    def nettx(self, interval=None):
        data = {"min": 0, "max": 100}
        query = self.make_query(
            "container_network_transmit_bytes_total",
            "sum(rate({}[2m]))/1024",
        )
        data["nettx"] = self.get_metrics(query)
        return {"data": data}

    def connections(self, interval=None):
        data = {"min": 0, "max": 100}
        query = self.make_query(
            "container_connections",
            "sum({}) by (destination)",
            query='state="ESTABLISHED",protocol="tcp"',
        )
        data['data'] = self.get_metrics(query, processor=self.connections_processor)
        return data

    def connections_processor(self, result):
        results = result['data']['result']
        data = {}
        for r in results:
            data[base.set_destination_hostname(r['metric']['destination'])] = self.default_processor(r['values'])
        return data

    def make_query(self, metric, agg, query="", container_name_label="container_name"):
        args = {
            "container_metric": metric,
            "app_name": self.app_name,
            "process_name": self.process_name or "",
            "container_name_label": container_name_label,
            "extra_query": query,
        }
        args["process_name_op"] = "=" if self.process_name else "!="
        result = []
        for tpl in self.app_metric_templates:
            result.append(agg.format(tpl.format(**args)))
        return ' or '.join(result)
