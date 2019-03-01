from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory

from tsuru_autoscale.instance.views import ListInstance, InstanceInfo

from tsuru_autoscale import settings
from importlib import import_module
import httpretty
from mock import patch, Mock

import os

class FakeAutoScaleClient(object):
    def __init__(self, instance={}, event={}):
        self.instance = Mock(**instance)
        self.event = Mock(**event)


class ListInstanceTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}       

    @patch.object(ListInstance, "client")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_list(self, token_is_valid, fake_client):
        token_is_valid.return_value = True

        json_mock = Mock()
        json_mock.json.return_value = [{"Name": "myinstance"}]

        fake_client = FakeAutoScaleClient(instance={"list.return_value": json_mock})

        response = ListInstance.as_view()(self.request)

        self.assertIn("instance/list.html", response.template_name)
        self.assertIn('list', response.context_data)
        ListInstance.client.instance.list.assert_called()



class InstanceInfoTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}       

    @patch("tsuru_dashboard.auth.views.token_is_valid")
    @patch.object(InstanceInfo, "client")
    def test_get_without_alarms(self, fake_client, token_is_valid):
        token_is_valid.return_value = True
        instance_attrs = {}

        json_mock = Mock()
        json_mock.json.return_value = {"Name": "instance"}
        instance_attrs["get.return_value"] = json_mock

        aresponse = Mock()
        aresponse.json.return_value = None
        instance_attrs["alarm_by_instance.return_value"] = aresponse

        fake_client = FakeAutoScaleClient(instance=instance_attrs)

        response = InstanceInfo.as_view()(self.request, name="myinstance")

        self.assertIn("instance/get.html", response.template_name)
        self.assertIn('item', response.context_data)
        self.assertIn('alarms', response.context_data)
        self.assertIn('events', response.context_data)
        InstanceInfo.client.instance.get.assert_called_with("myinstance")

    @patch("tsuru_dashboard.auth.views.token_is_valid")
    @patch.object(InstanceInfo, "client")
    def test_get(self, fake_client, token_is_valid):
        json_mock = Mock()
        json_mock.json.return_value = {"Name": "myinstance"}
        instance_attrs = {"get.return_value": json_mock}
        fake_client = FakeAutoScaleClient(instance=instance_attrs)
        token_is_valid.return_value = True

        response = InstanceInfo.as_view()(self.request, name="myinstance")

        self.assertIn("instance/get.html", response.template_name)
        self.assertIn('item', response.context_data)
        self.assertIn('alarms', response.context_data)
        self.assertIn('events', response.context_data)
        InstanceInfo.client.instance.get.assert_called_with("myinstance")
