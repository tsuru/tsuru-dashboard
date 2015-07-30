from django.test import TestCase
from django.core.urlresolvers import reverse

from mock import patch

from autoscale.context_processors import autoscale_enabled

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
    @patch("auth.views.token_is_valid")
    def test_index(self, token_is_valid):
        token_is_valid.return_value = True
        with self.settings(SESSION_ENGINE='django.contrib.sessions.backends.file'):
            session = self.client.session
            session['tsuru_token'] = "beare token"
            session.save()

            response = self.client.get(reverse("autoscale"))
            self.assertTemplateUsed(response, "autoscale/index.html")

    @patch("auth.views.token_is_valid")
    def test_service_url(self, token_is_valid):
        token_is_valid.return_value = True

        autoscale_dashboard_url = "http://localhost:123"
        os.environ["AUTOSCALE_DASHBOARD_URL"] = autoscale_dashboard_url
        session_engine = "django.contrib.sessions.backends.file"
        token = "token/+12faslfkl12"

        with self.settings(SESSION_ENGINE=session_engine):
            session = self.client.session
            session['tsuru_token'] = "beare {}".format(token)
            session.save()

            response = self.client.get(reverse("autoscale"))
            expected = "{}?TSURU_TOKEN={}".format(autoscale_dashboard_url, urllib.quote(token))
            self.assertEqual(response.context_data["service_url"], expected)
