import os

import requests


def host():
    return os.environ.get("AUTOSCALE_HOST", "")


def list(alarm_name, token):
    url = "{}/alarm/{}/event".format(host(), alarm_name)
    headers = {"Authorization": token}
    response = requests.get(url, headers=headers)
    return response
