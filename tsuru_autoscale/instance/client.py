import os
import logging

import requests

from tsuru_autoscale import settings


def list(token):
    url = "{}/service/instance".format(settings.AUTOSCALE_HOST)
    headers = {"Authorization": token}
    logging.debug("trying to get service instances - {}".format(url))
    response = requests.get(url, headers=headers)
    logging.debug("service instances response - {}".format(response))
    return response


def get(name, token):
    url = "{}/service/instance/{}".format(settings.AUTOSCALE_HOST, name)
    headers = {"Authorization": token}
    response = requests.get(url, headers=headers)
    return response


def alarms_by_instance(instance, token):
    url = "{}/alarm/instance/{}".format(settings.AUTOSCALE_HOST, instance)
    headers = {"Authorization": token}
    response = requests.get(url, headers=headers)
    return response
