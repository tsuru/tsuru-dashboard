import os
import json
import logging

import requests


def host():
    return os.environ.get("AUTOSCALE_HOST", "")


def new(data, token):
    url = "{}/datasource".format(host())
    headers = {"Authorization": token}
    d = json.dumps(data)
    logging.error("trying to add new datasource - {} - {}".format(url, d))
    response = requests.post(url, data=d, headers=headers)
    logging.error("add new datasource response - {}".format(response))
    return response


def list(token):
    url = "{}/datasource?public=true".format(host())
    headers = {"Authorization": token}
    response = requests.get(url, headers=headers)
    return response


def remove(name, token):
    url = "{}/datasource/{}".format(host(), name)
    headers = {"Authorization": token}
    response = requests.delete(url, headers=headers)
    return response


def get(name, token):
    url = "{}/datasource/{}".format(host(), name)
    headers = {"Authorization": token}
    response = requests.get(url, headers=headers)
    return response
