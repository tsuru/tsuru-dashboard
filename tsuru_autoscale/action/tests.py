from django.test import TestCase
from django.core.urlresolvers import reverse

from tsuru_autoscale.action.forms import ActionForm
from tsuru_autoscale.action import client

import httpretty
import mock

import os


class RemoveTestCase(TestCase):
    @mock.patch("tsuru_autoscale.action.client.list")
    @mock.patch("tsuru_autoscale.action.client.remove")
    def test_new_post(self, remove_mock, list_mock):
        url = "{}?TSURU_TOKEN=bla".format(reverse("action-remove", args=["name"]))
        response = self.client.delete(url)

        url = "{}?TSURU_TOKEN=bla".format(reverse("action-list"))
        self.assertRedirects(response, url)
        remove_mock.assert_called_with("name", "bla")


class NewTestCase(TestCase):
    def test_new(self):
        url = "{}?TSURU_TOKEN=bla".format(reverse("action-new"))
        response = self.client.get(url)
        self.assertTemplateUsed(response, "action/new.html")
        self.assertIsInstance(response.context['form'], ActionForm)
        self.assertFalse(response.context['form'].is_bound)

    def test_new_invalid_post(self):
        url = "{}?TSURU_TOKEN=bla".format(reverse("action-new"))
        response = self.client.post(url, {})
        self.assertFalse(response.context['form'].is_valid())

    @mock.patch("tsuru_autoscale.action.client.list")
    @mock.patch("tsuru_autoscale.action.client.new")
    def test_new_post(self, new_mock, list_mock):
        data = {
            'url': u'someurl',
            'body': u'',
            'headers': u'',
            'name': u'name',
            'method': u'GET',
        }

        url = "{}?TSURU_TOKEN=bla".format(reverse("action-new"))
        response = self.client.post(url, data)

        url = "{}?TSURU_TOKEN=bla".format(reverse("action-list"))
        self.assertRedirects(response, url)
        new_mock.assert_called_with(data, "bla")


class ListTestCase(TestCase):
    @mock.patch("tsuru_autoscale.action.client.list")
    def test_list(self, list_mock):
        url = "{}?TSURU_TOKEN=bla".format(reverse("action-list"))
        response = self.client.get(url)

        self.assertTemplateUsed(response, "action/list.html")
        self.assertIn('list', response.context)
        list_mock.assert_called_with("bla")


class GetTestCase(TestCase):
    @mock.patch("tsuru_autoscale.action.client.get")
    def test_get(self, get_mock):
        result_mock = mock.Mock()
        result_mock.json.return_value = {"Name": "ble"}
        get_mock.return_value = result_mock

        url = "{}?TSURU_TOKEN=bla".format(reverse("action-get", args=["name"]))
        response = self.client.get(url)

        self.assertTemplateUsed(response, "action/get.html")
        self.assertIn('item', response.context)
        get_mock.assert_called_with("name", "bla")


class ClientTestCase(TestCase):
    def setUp(self):
        httpretty.enable()

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    def test_list(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.GET,
            "http://autoscalehost.com/action",
        )

        client.list("token")

    def test_new(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.POST,
            "http://autoscalehost.com/action",
        )

        client.new({}, "token")

    def test_remove(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.DELETE,
            "http://autoscalehost.com/action/name",
        )

        client.remove("name", "token")

    def test_get(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.GET,
            "http://autoscalehost.com/action/name",
            "result",
        )

        result = client.get("name", "token")
        self.assertEqual(result.text, "result")


class ActionFormTestCase(TestCase):
    def test_required_fields(self):
        fields = {
            "url": True,
            "method": True,
            "name": True,
            "body": False,
            "headers": False,
        }

        form = ActionForm()

        for field, required in fields.items():
            self.assertEqual(form.fields[field].required, required)
