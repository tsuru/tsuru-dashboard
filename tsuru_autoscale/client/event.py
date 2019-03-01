import os
import requests


class EventClient(object):
    def __init__(self, target, token):
        self.target = target
        self.token = token

    def list(self, alarm_name):
        url = "{}/alarm/{}/event".format(self.target, alarm_name)
        headers = {"Authorization": self.token}
        response = requests.get(url, headers=headers)
        return response
