import os
import json

import requests


def host():
    return os.environ.get("AUTOSCALE_HOST", "")


def new(data, token):
    url = "{}/alarm".format(host())
    headers = {"Authorization": token}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response


def list(token):
    url = "{}/alarm".format(host())
    headers = {"Authorization": token}
    response = requests.get(url, headers=headers)
    return response


def remove(name, token):
    url = "{}/alarm/{}".format(host(), name)
    headers = {"Authorization": token}
    response = requests.delete(url, headers=headers)
    return response


def get(name, token):
    url = "{}/alarm/{}".format(host(), name)
    headers = {"Authorization": token}
    response = requests.get(url, headers=headers)
    return response


def service_instance_list(token):
    url = "{}/service/instance".format(host())
    headers = {"Authorization": token}
    response = requests.get(url, headers=headers)
    return response
