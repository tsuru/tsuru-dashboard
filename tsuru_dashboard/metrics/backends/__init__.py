from tsuru_dashboard import settings
from tsuru_dashboard.metrics.backends.elasticsearch import AppBackend

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
    app["envs"] = get_envs(app_name, token)
    return AppBackend(app=app, token=token, **kwargs)
