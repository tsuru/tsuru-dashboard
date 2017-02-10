from django.http import HttpResponse, HttpResponseBadRequest
from urlparse import urlparse

from tsuru_dashboard import settings
from tsuru_dashboard.auth.views import LoginRequiredView
from .backends.elasticsearch import NodeMetricsBackend, NodesMetricsBackend
from .backends import get_app_backend, get_tsuru_backend
import json
import requests


class Metric(LoginRequiredView):
    def get(self, *args, **kwargs):
        token = self.request.session.get('tsuru_token')
        metric = self.request.GET.get("metric")
        if not metric:
            return HttpResponseBadRequest()

        interval = self.request.GET.get("interval")
        date_range = self.request.GET.get("date_range")
        target = kwargs['target']

        backends = self.get_metrics_backend(metric=metric, target=target, date_range=date_range, token=token)
        if backends is None:
            return HttpResponseBadRequest()

        if not isinstance(backends, list):
            backends = [backends]

        data = {}
        for backend in backends:
            try:
                data = getattr(backend, metric)(interval=interval)
            except:
                continue
            if isinstance(data, dict) and len(data["data"]) > 0:
                data["source"] = backend.url
                break

        return HttpResponse(json.dumps(data))


class AppMetric(Metric):
    def get_metrics_backend(self, metric, target, date_range, token):
        process_name = self.request.GET.get("process_name")
        return get_app_backend(app_name=target, token=token, date_range=date_range, process_name=process_name)


class ComponentMetric(Metric):
    def get_metrics_backend(self, metric, target, date_range, token):
        return get_tsuru_backend(component=target, token=token, date_range=date_range)


class NodeMetric(Metric):
    def get_metrics_backend(self, metric, target, date_range, token):
        return NodeMetricsBackend(addr=target, date_range=date_range)


class PoolMetric(Metric):
    def extract_ip(self, address):
        if not urlparse(address).scheme:
            address = "http://"+address
        return urlparse(address).hostname

    def get_pool_nodes(self, pool_name):
        url = "{}/docker/node".format(settings.TSURU_HOST)
        response = requests.get(url, headers=self.authorization)
        pool_nodes = []
        if response.status_code != 204:
            nodes = response.json().get("nodes", [])

            for node in nodes:
                if node["Metadata"].get("pool", "") == pool_name:
                    addr = self.extract_ip(node["Address"])
                    pool_nodes.append(addr)

        return pool_nodes

    def get_metrics_backend(self, metric, target, date_range, token):
        addrs = self.get_pool_nodes(target)
        return NodesMetricsBackend(addrs=addrs, date_range=date_range)
