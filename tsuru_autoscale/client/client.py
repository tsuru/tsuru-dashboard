from tsuru_autoscale.client.instance import InstanceClient
from tsuru_autoscale.client.event import EventClient



class Client(object):
    def __init__(self, target, token):
        self.instance = InstanceClient(target, token)
        self.event = EventClient(target, token)