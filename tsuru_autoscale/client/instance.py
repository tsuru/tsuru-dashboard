import os
import logging
import requests

class InstanceClient(object):
	def __init__(self, target, token):
		self.target = target
		self.token = token

	def list(self):
		url = "{}/service/instance".format(self.target)
		headers = {"Authorization": self.token}
		logging.debug("trying to get service instances - {}".format(url))
		response = requests.get(url, headers=headers)
		logging.debug("service instances response - {}".format(response))
		return response


	def get(self, name):
		url = "{}/service/instance/{}".format(self.target, name)
		headers = {"Authorization": self.token}
		response = requests.get(url, headers=headers)
		return response


	def alarms_by_instance(self, instance):
		url = "{}/alarm/instance/{}".format(self.target, instance)
		headers = {"Authorization": self.token}
		response = requests.get(url, headers=headers)
		return response
