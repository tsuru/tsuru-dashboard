from tsuru_dashboard import settings
from tsuru_dashboard.metrics.backends import elasticsearch, prometheus
from tsuru_dashboard.metrics.backends import base

import requests


def get_app(app_name, token):
    url = '{}/apps/{}'.format(settings.TSURU_HOST, app_name)
    headers = {"authorization": token}
    return requests.get(url, headers=headers).json()


def get_envs(app_name, token):
    url = '{}/apps/{}/env'.format(settings.TSURU_HOST, app_name)
    headers = {"authorization": token}
    data = requests.get(url, headers=headers).json()
    envs = {}
    for env in data:
        envs[env['name']] = env['value']

    return envs


def get_app_backend(app_name, token, **kwargs):
    app = get_app(app_name, token)
    envs = base.get_envs_from_api(app, token)
    url = ""

    if envs and "METRICS_PROMETHEUS_HOST" in envs:
        url = envs["METRICS_PROMETHEUS_HOST"]
        return prometheus.AppBackend(app=app, url=url, **kwargs)

    if envs and "METRICS_ELASTICSEARCH_HOST" in envs:
        url = envs["METRICS_ELASTICSEARCH_HOST"]
        return elasticsearch.AppBackend(app=app, url=url, **kwargs)

    if not url:
        app["envs"] = get_envs(app_name, token)
        if "envs" in app and "ELASTICSEARCH_HOST" in app["envs"]:
            url = app["envs"]["ELASTICSEARCH_HOST"]

    return elasticsearch.AppBackend(app=app, url=url, **kwargs)
