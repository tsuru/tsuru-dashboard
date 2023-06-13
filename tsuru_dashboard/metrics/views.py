from django.http import HttpResponse, HttpResponseBadRequest
from urlparse import urlparse

from tsuru_dashboard import settings
from tsuru_dashboard.auth.views import LoginRequiredView
from .backends import get_app_backend, get_tsuru_backend
import json
import logging

logger = logging.getLogger(__name__)


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
                logger.exception("unable query backend")
                continue
            if isinstance(data, dict) and len(data["data"]) > 0:
                data["source"] = backend.url
                break

        return HttpResponse(json.dumps(data))


class AppMetric(Metric):
    def get_metrics_backend(self, metric, target, date_range, token):
        process_name = self.request.GET.get("process_name")
        return get_app_backend(app_name=target, token=token, date_range=date_range, process_name=process_name)
