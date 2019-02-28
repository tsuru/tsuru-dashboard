from django.test import TestCase
from django.core.urlresolvers import reverse, resolve
from django.conf import settings

from tsuru_autoscale.wizard import forms
from tsuru_autoscale.wizard import client

from importlib import import_module

import mock
import httpretty
import os


class ScaleFormTest(TestCase):
    def test_required_fields(self):
        fields = {
            "metric": True,
            "operator": True,
            "value": True,
            "step": True,
            "wait": True,
            "aggregator": True,
        }

        form = forms.ScaleForm()

        for field, required in fields.items():
            self.assertEqual(form.fields[field].required, required)


class ConfigFormTest(TestCase):
    def test_required_fields(self):
        fields = {
            "min": True,
        }

        form = forms.ConfigForm()

        for field, required in fields.items():
            self.assertEqual(form.fields[field].required, required)


class IndexTestCase(TestCase):
    def setUp(self):
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.session = store
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
        self.session["tsuru_token"] = "b bla"
        self.session.save()

    @mock.patch("tsuru_autoscale.wizard.views.process_list")
    @mock.patch("tsuru_autoscale.datasource.client.list")
    def test_index(self, dlist_mock, process_mock):
        url = "{}?TSURU_TOKEN=bla".format(reverse("wizard-new", args=["instance"]))
        response = self.client.get(url)
        self.assertTemplateUsed(response, "wizard/index.html")

    @mock.patch("tsuru_autoscale.wizard.views.process_list")
    @mock.patch("tsuru_autoscale.datasource.client.list")
    def test_forms_prefix(self, dlist_mock, process_mock):
        url = "{}?TSURU_TOKEN=bla".format(reverse("wizard-new", args=["instance"]))
        response = self.client.get(url)

        forms = {
            "scale_up_form": "scale_up",
            "scale_down_form": "scale_down",
        }

        for f, prefix in forms.items():
            self.assertEqual(response.context[f].prefix, prefix)

    @mock.patch("tsuru_autoscale.wizard.views.process_list")
    @mock.patch("tsuru_autoscale.datasource.client.list")
    def test_config_process_list(self, dlist_mock, process_mock):
        process = [("web", "web")]
        process_mock.return_value = process

        url = "{}?TSURU_TOKEN=bla".format(reverse("wizard-new", args=["instance"]))
        response = self.client.get(url)

        choices = response.context["config_form"].fields["process"].choices
        self.assertListEqual(process, choices)

    @mock.patch("tsuru_autoscale.wizard.views.process_list")
    @mock.patch("tsuru_autoscale.datasource.client.list")
    def test_scale_metrics(self, dlist_mock, process_mock):
        data = [{"Name": "cpu"}, {"Name": "mem"}]
        response_mock = mock.Mock()
        response_mock.json.return_value = data
        dlist_mock.return_value = response_mock

        url = "{}?TSURU_TOKEN=bla".format(reverse("wizard-new", args=["instance"]))
        response = self.client.get(url)

        expected_choices = [("cpu", "cpu"), ("mem", "mem")]

        choices = response.context["scale_up_form"].fields["metric"].choices
        self.assertListEqual(expected_choices, choices)

        choices = response.context["scale_down_form"].fields["metric"].choices
        self.assertListEqual(expected_choices, choices)


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
            "http://autoscalehost.com/wizard",
        )

        client.new({}, "token")

    def test_get(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.GET,
            "http://autoscalehost.com/wizard/name",
        )

        client.get("name", "token")

    def test_events(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.GET,
            "http://autoscalehost.com/wizard/name/events",
        )

        client.events("name", "token")

    def test_remove(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.DELETE,
            "http://autoscalehost.com/wizard/name",
        )

        client.remove("name", "token")


class RemoveTestCase(TestCase):
    def setUp(self):
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.session = store
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
        self.session["tsuru_token"] = "testtoken"
        self.session.save()

    @mock.patch("tsuru_autoscale.wizard.client.remove")
    def test_remove(self, remove_mock):
        url = reverse("wizard-remove", args=["name"])
    #    url = "{}?TSURU_TOKEN=bla".format(reverse("wizard-remove", args=["name"]))
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'wizard-remove')

        response = self.client.get(url)
        print(response)
        remove_mock.assert_called_with("name", "bla")
        url = reverse("autoscale-app-info", args=["name"])
        self.assertIn(url, response.url)

    @mock.patch("tsuru_autoscale.wizard.client.enable")
    def test_enable(self, enable_mock):
        url = reverse("wizard-enable", args=["name"])
        response = self.client.get(url)

        url = reverse("autoscale-app-info", args=["name"])
        self.assertIn(url, response.url)
        enable_mock.assert_called_with("name", "bla")

    @mock.patch("tsuru_autoscale.wizard.client.disable")
    def test_disable(self, disable_mock):
        url = reverse("wizard-disable", args=["name"])
        response = self.client.get(url)

        url = reverse("autoscale-app-info", args=["name"])
        self.assertIn(url, response.url)
        disable_mock.assert_called_with("name", "bla")
