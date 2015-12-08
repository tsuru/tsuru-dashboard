from django.test import TestCase
from django.core.urlresolvers import reverse

from mock import patch, Mock

from tsuru_dashboard.autoscale.context_processors import autoscale_enabled

import os
import urllib


class ContextProcesssorsTest(TestCase):
    def test_autoscale_enabled(self):
        os.environ["AUTOSCALE_DASHBOARD_URL"] = "http://localhost"
        result = autoscale_enabled({})
        self.assertTrue(result["autoscale_enabled"])

    def test_autoscale_not_enabled(self):
        del os.environ["AUTOSCALE_DASHBOARD_URL"]
        result = autoscale_enabled({})
        self.assertFalse(result["autoscale_enabled"])


class IndexTestCase(TestCase):
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    @patch("requests.get")
    def test_index(self, get_mock, token_is_valid):
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = {"name": "appname"}
        get_mock.return_value = response_mock
        token_is_valid.return_value = True

        with self.settings(SESSION_ENGINE='django.contrib.sessions.backends.file'):
            session = self.client.session
            session['tsuru_token'] = "beare token"
            session.save()

            response = self.client.get(reverse("autoscale", args=["app"]))
            self.assertTemplateUsed(response, "autoscale/index.html")

    @patch("tsuru_dashboard.auth.views.token_is_valid")
    @patch("requests.get")
    def test_service_url(self, get_mock, token_is_valid):
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = {"name": "app"}
        get_mock.return_value = response_mock

        token_is_valid.return_value = True

        autoscale_dashboard_url = "http://localhost:123"
        os.environ["AUTOSCALE_DASHBOARD_URL"] = autoscale_dashboard_url
        session_engine = "django.contrib.sessions.backends.file"
        token = "token/+12faslfkl12"

        with self.settings(SESSION_ENGINE=session_engine):
            session = self.client.session
            session['tsuru_token'] = "beare {}".format(token)
            session.save()

            response = self.client.get(reverse("autoscale", args=["app"]))
            expected = "{}/app/{}?TSURU_TOKEN={}".format(
                autoscale_dashboard_url, "app", token)
            self.assertEqual(urllib.unquote(response.context_data["service_url"]), expected)

    @patch("tsuru_dashboard.auth.views.token_is_valid")
    @patch("requests.get")
    def test_app_not_found(self, get_mock, token_is_valid):
        response_mock = Mock(status_code=404)
        get_mock.return_value = response_mock
        token_is_valid.return_value = True

        with self.settings(SESSION_ENGINE='django.contrib.sessions.backends.file'):
            session = self.client.session
            session['tsuru_token'] = "beare token"
            session.save()

            response = self.client.get(reverse("autoscale", args=["app"]))
            self.assertEqual(response.status_code, 404)
