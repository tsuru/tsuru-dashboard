import os
import json


TSURU_HOST = os.environ.get("TSURU_HOST", "http://localhost:8080")
ELASTICSEARCH_HOST = os.environ.get("ELASTICSEARCH_HOST")
PROMETHEUS_HOST = os.environ.get("PROMETHEUS_HOST")
ELASTICSEARCH_INDEX = os.environ.get("ELASTICSEARCH_INDEX", ".measures-tsuru")
METRICS_COMPONENTS = os.environ.get("METRICS_COMPONENTS", "registry, big-sibling")
RESOLVE_CONNECTION_HOSTS = os.environ.get("RESOLVE_CONNECTION_HOSTS", "") in ['true', 'True', '1']
ELASTICSEARCH_METRICS_ENABLED = os.environ.get("ELASTICSEARCH_METRICS_ENABLED", "true") in ['true', 'True', '1']

GRAFANA_DASHBOARD = os.environ.get("GRAFANA_DASHBOARD")
GRAFANA_POOL_DASHBOARD = os.environ.get("GRAFANA_POOL_DASHBOARD")
GRAFANA_THEME = os.environ.get("GRAFANA_THEME", "light")
GRAFANA_KIOSK = os.environ.get("GRAFANA_KIOSK", "tv")
GRAFANA_DEFAULT_DATASOURCE = os.environ.get("GRAFANA_DEFAULT_DATASOURCE")
GRAFANA_DATASOURCE_FOR_POOL = json.loads(os.environ.get("GRAFANA_DATASOURCE_FOR_POOL", "{}"))
