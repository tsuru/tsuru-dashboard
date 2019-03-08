from django.test import TestCase, override_settings
from django.core.urlresolvers import reverse

from tsuru_autoscale.wizard import forms
from tsuru_autoscale.wizard import client


from django.test.client import RequestFactory
from mock import patch, Mock
from tsuru_autoscale.wizard.views import Wizard, WizardRemove, WizardEnable, WizardDisable


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


@patch("tsuru_dashboard.auth.views.token_is_valid", return_value=True)
@patch.object(Wizard, "client")
class WizardTestCase(TestCase):
    def setUp(self):
        self.view = Wizard()
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}   

    def test_index(self, fake_client, token_is_valid):
        self.view.process_list = Mock()
        response = self.view.get(self.request, instance="myinstance")
        self.assertIn("wizard/index.html", response.template_name)

    def test_forms_prefix(self, fake_client, token_is_valid):
        self.view.process_list = Mock()
        response = self.view.get(self.request, instance="myinstance")
        forms = {
            "scale_up_form": "scale_up",
            "scale_down_form": "scale_down",
        }

        for f, prefix in forms.items():
            self.assertEqual(response.context_data[f].prefix, prefix)

    def test_config_process_list(self, fake_client, token_is_valid):
        process = [("web", "web")]
        self.view.process_list = lambda r: process

        response = self.view.get(self.request, instance="myinstance")

        choices = response.context_data["config_form"].fields["process"].choices
        self.assertListEqual(process, choices)

    def test_scale_metrics(self, fake_client, token_is_valid):
        data = [{"Name": "cpu"}, {"Name": "mem"}]
        response_mock = Mock()
        response_mock.json.return_value = data
        fake_client.datasource.list.return_value = response_mock

        self.view.process_list = Mock()
        response = self.view.get(self.request, instance="myinstance")

        expected_choices = [("cpu", "cpu"), ("mem", "mem")]

        choices = response.context_data["scale_up_form"].fields["metric"].choices
        self.assertListEqual(expected_choices, choices)

        choices = response.context_data["scale_down_form"].fields["metric"].choices
        self.assertListEqual(expected_choices, choices)


class WizardRemoveTestCase(TestCase):
    @patch("tsuru_dashboard.auth.views.token_is_valid", return_value=True)
    @patch.object(WizardRemove, "client")
    def test_remove(self, fake_client, token_is_valid):
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}   
        
        response = WizardRemove.as_view()(request, instance="name")
        fake_client.wizard.remove.assert_called_with("name")
        url = reverse("autoscale-app-info", args=["name"])

        self.assertIn(url, response.url)


class WizardEnableTestCase(TestCase):
    @patch("tsuru_dashboard.auth.views.token_is_valid", return_value=True)
    @patch.object(WizardEnable, "client")
    def test_enable(self, fake_client, token_is_valid):
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}   
        
        response = WizardEnable.as_view()(request, instance="name")

        url = reverse("autoscale-app-info", args=["name"])
        self.assertIn(url, response.url)
        fake_client.wizard.enable.assert_called_with("name")


class WizardDisableTestCase(TestCase):
    @patch("tsuru_dashboard.auth.views.token_is_valid", return_value=True)
    @patch.object(WizardDisable, "client")
    def test_disable(self, fake_client, token_is_valid):
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}   
        
        response = WizardDisable.as_view()(request, instance="name")

        url = reverse("autoscale-app-info", args=["name"])
        self.assertIn(url, response.url)
        fake_client.wizard.disable.assert_called_with("name")
