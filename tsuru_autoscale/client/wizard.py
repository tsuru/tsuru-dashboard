import os
import json
import requests


class WizardClient(object):
    def __init__(self, target, token):
        self.target = target
        self.token = token

    def new(self, data):
        url = "{}/wizard".format(self.target)
        headers = {"Authorization": self.token}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response


    def get(self, name):
        url = "{}/wizard/{}".format(self.target, name)
        headers = {"Authorization": self.token}
        response = requests.get(url, headers=headers)
        return response


    def remove(self, name):
        url = "{}/wizard/{}".format(self.target, name)
        headers = {"Authorization": self.token}
        response = requests.delete(url, headers=headers)
        return response


    def enable(self, name):
        url = "{}/wizard/{}/enable".format(self.target, name)
        headers = {"Authorization": self.token}
        response = requests.post(url, headers=headers)
        return response


    def disable(self, name):
        url = "{}/wizard/{}/disable".format(self.target, name)
        headers = {"Authorization": self.token}
        response = requests.post(url, headers=headers)
        return response


    def events(self, name):
        url = "{}/wizard/{}/events".format(self.target, name)
        headers = {"Authorization": self.token}
        response = requests.get(url, headers=headers)
        return response
