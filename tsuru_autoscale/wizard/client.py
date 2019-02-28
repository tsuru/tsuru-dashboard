import os
import json

import requests


def host():
    return os.environ.get("AUTOSCALE_HOST", "")


def new(data, token):
    url = "{}/wizard".format(host())
    headers = {"Authorization": token}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response


def get(name, token):
    url = "{}/wizard/{}".format(host(), name)
    headers = {"Authorization": token}
    response = requests.get(url, headers=headers)
    return response


def remove(name, token):
    url = "{}/wizard/{}".format(host(), name)
    headers = {"Authorization": token}
    response = requests.delete(url, headers=headers)
    return response


def enable(name, token):
    url = "{}/wizard/{}/enable".format(host(), name)
    headers = {"Authorization": token}
    response = requests.post(url, headers=headers)
    return response


def disable(name, token):
    url = "{}/wizard/{}/disable".format(host(), name)
    headers = {"Authorization": token}
    response = requests.post(url, headers=headers)
    return response


def events(name, token):
    url = "{}/wizard/{}/events".format(host(), name)
    headers = {"Authorization": token}
    response = requests.get(url, headers=headers)
    return response
