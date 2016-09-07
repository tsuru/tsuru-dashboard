from tsuru_dashboard import settings

import requests


class MetricNotEnabled(Exception):
    pass


def get_envs_from_api(app, token):
    headers = {'authorization': token}
    url = "{}/apps/{}/metric/envs".format(settings.TSURU_HOST, app["name"])
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None
