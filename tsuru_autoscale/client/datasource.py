import os
import json
import requests
import logging


class DatasourceClient(object):
    def __init__(self, target, token):
        self.target = target
        self.token = token

    def new(self, data):
        url = "{}/datasource".format(self.target)
        headers = {"Authorization": self.token}
        d = json.dumps(data)
        logging.error("trying to add new datasource - {} - {}".format(url, d))
        response = requests.post(url, data=d, headers=headers)
        logging.error("add new datasource response - {}".format(response))
        return response


    def list(self):
        url = "{}/datasource?public=true".format(self.target)
        headers = {"Authorization": self.token}
        response = requests.get(url, headers=headers)
        return response


    def remove(self, name):
        url = "{}/datasource/{}".format(self.target, name)
        headers = {"Authorization": self.token}
        response = requests.delete(url, headers=headers)
        return response


    def get(self, name):
        url = "{}/datasource/{}".format(self.target, name)
        headers = {"Authorization": self.token}
        response = requests.get(url, headers=headers)
        return response
