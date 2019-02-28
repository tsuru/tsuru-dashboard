from django.test import TestCase
from django.core.urlresolvers import reverse

from tsuru_autoscale.alarm.forms import AlarmForm
from tsuru_autoscale.alarm import client

import httpretty
import mock

import os


class RemoveTestCase(TestCase):
    @mock.patch("tsuru_autoscale.alarm.client.list")
    @mock.patch("tsuru_autoscale.alarm.client.remove")
    def test_remove(self, remove_mock, list_mock):
        url = "{}?TSURU_TOKEN=bla".format(reverse("alarm-remove", args=["name"]))
        response = self.client.delete(url)

        url = "{}?TSURU_TOKEN=bla".format(reverse("alarm-list"))
        self.assertRedirects(response, url)
        remove_mock.assert_called_with("name", "bla")


class NewTestCase(TestCase):
    @mock.patch("tsuru_autoscale.alarm.client.service_instance_list")
    @mock.patch("tsuru_autoscale.datasource.client")
    @mock.patch("tsuru_autoscale.action.client")
    def test_new(self, ds_client_mock, a_client_mock, sil):
        url = "{}?TSURU_TOKEN=bla".format(reverse("alarm-new"))
        response = self.client.get(url)
        self.assertTemplateUsed(response, "alarm/new.html")
        self.assertIsInstance(response.context['form'], AlarmForm)
        self.assertFalse(response.context['form'].is_bound)

    @mock.patch("tsuru_autoscale.alarm.client.service_instance_list")
    @mock.patch("tsuru_autoscale.datasource.client")
    @mock.patch("tsuru_autoscale.action.client")
    def test_new_invalid_post(self, ds_client_mock, a_client_mock, sli):
        url = "{}?TSURU_TOKEN=bla".format(reverse("alarm-new"))
        response = self.client.post(url, {})
        self.assertFalse(response.context['form'].is_valid())

    @mock.patch("tsuru_autoscale.alarm.client.service_instance_list")
    @mock.patch("tsuru_autoscale.action.client")
    @mock.patch("tsuru_autoscale.datasource.client")
    @mock.patch("tsuru_autoscale.alarm.client.list")
    @mock.patch("tsuru_autoscale.alarm.client.new")
    def test_new_post(self, new_mock, list_mock, ds_client_mock, a_client_mock, sil):
        json_mock = mock.Mock()
        json_mock.json.return_value = [{"Name": "bla"}]
        sil.return_value = json_mock

        json_mock = mock.Mock()
        json_mock.json.return_value = [{"Name": "bla"}]
        a_client_mock.list.return_value = json_mock

        json_mock = mock.Mock()
        json_mock.json.return_value = [{"Name": "bla"}]
        ds_client_mock.list.return_value = json_mock
        data = {
            'name': u'name',
            'expression': u'x > 10',
            'enabled': True,
            'wait': 10,
            'datasource': 'bla',
            'actions': ['bla'],
            'instance': 'bla',
        }

        url = "{}?TSURU_TOKEN=bla".format(reverse("alarm-new"))
        response = self.client.post(url, data)

        url = "{}?TSURU_TOKEN=bla".format(reverse("alarm-list"))
        self.assertRedirects(response, url)
        new_mock.assert_called_with(data, "bla")


class ListTestCase(TestCase):
    @mock.patch("tsuru_autoscale.alarm.client.list")
    def test_list(self, list_mock):
        url = "{}?TSURU_TOKEN=bla".format(reverse("alarm-list"))
        response = self.client.get(url)

        self.assertTemplateUsed(response, "alarm/list.html")
        self.assertIn('list', response.context)
        list_mock.assert_called_with("bla")


class GetTestCase(TestCase):
    @mock.patch("tsuru_autoscale.alarm.client.get")
    def test_get(self, get_mock):
        result_mock = mock.Mock()
        result_mock.json.return_value = {"name": "ble"}
        get_mock.return_value = result_mock

        url = "{}?TSURU_TOKEN=bla".format(reverse("alarm-get", args=["ble"]))
        response = self.client.get(url)

        self.assertTemplateUsed(response, "alarm/get.html")
        self.assertIn('item', response.context)
        get_mock.assert_called_with("ble", "bla")


class ClientTestCase(TestCase):
    def setUp(self):
        httpretty.enable()

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    def test_new(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.POST,
            "http://autoscalehost.com/alarm",
        )

        client.new({}, "token")

    def test_list(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.GET,
            "http://autoscalehost.com/alarm",
        )

        client.list("token")

    def test_remove(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.DELETE,
            "http://autoscalehost.com/alarm/name",
        )

        client.remove("name", "token")

    def test_get(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.GET,
            "http://autoscalehost.com/alarm/name",
            "result",
        )

        result = client.get("name", "token")
        self.assertEqual(result.text, "result")


class AlarmFormTestCase(TestCase):
    def test_required_fields(self):
        fields = {
            "name": True,
            "expression": True,
            "enabled": True,
            "wait": True,
        }

        form = AlarmForm()

        for field, required in fields.items():
            self.assertEqual(form.fields[field].required, required)
