from tsuru_dashboard import settings

import requests

import socket


class MetricNotEnabled(Exception):
    pass


def get_envs_from_api(app, token):
    headers = {'authorization': token}
    url = "{}/apps/{}/metric/envs".format(settings.TSURU_HOST, app["name"])
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None


def set_destination_hostname(destination):
    if not settings.RESOLVE_CONNECTION_HOSTS:
        return destination
    ipport = destination.rsplit(':', 1)
    try:
        host, _, _ = socket.gethostbyaddr(ipport[0])
        return "{}({})".format(destination, host)
    except socket.error:
        pass
    return destination
