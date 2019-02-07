from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings

from importlib import import_module
from tsuru_dashboard import settings as tsuru_settings

from mock import patch, Mock


class NodeRemoveViewTest(TestCase):
    def setUp(self):
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.session = store
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key

    @patch("requests.get")
    @patch("requests.delete")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_remove_node_with_default_params(self, token_is_valid, delete, get):
        token_is_valid.return_value = True

        response_mock = Mock(status_code=200)
        delete.return_value = response_mock

        self.session["tsuru_token"] = "admin"
        self.session.save()

        response = self.client.delete(
            reverse("node-remove", kwargs={"address": "http://localhost:2345"}))

        self.assertEqual(200, response.status_code)

        api_url = "{}/docker/node/http://localhost:2345".format(tsuru_settings.TSURU_HOST)
        query = "?remove-iaas=false&no-rebalance=true"
        headers = {'authorization': u'admin'}
        delete.assert_called_with(api_url + query, headers=headers)

    @patch("requests.get")
    @patch("requests.delete")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_remove_node_with_destroy_and_rebalance_true(self, token_is_valid, delete, get):
        token_is_valid.return_value = True

        response_mock = Mock(status_code=200)
        delete.return_value = response_mock

        self.session["tsuru_token"] = "admin"
        self.session.save()

        url = reverse("node-remove", kwargs={"address": "http://localhost:2345"})
        response = self.client.delete(url, data="rebalance=true&destroy=true")

        self.assertEqual(200, response.status_code)

        api_url = "{}/docker/node/http://localhost:2345".format(tsuru_settings.TSURU_HOST)
        query = "?remove-iaas=true&no-rebalance=false"
        headers = {'authorization': u'admin'}
        delete.assert_called_with(api_url + query, headers=headers)

    @patch("requests.get")
    @patch("requests.delete")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_remove_node_with_destroy_and_rebalance_false(self, token_is_valid, delete, get):
        token_is_valid.return_value = True

        response_mock = Mock(status_code=204)
        delete.return_value = response_mock

        self.session["tsuru_token"] = "admin"
        self.session.save()

        url = reverse("node-remove", kwargs={"address": "http://localhost:2345"})
        response = self.client.delete(url, data="rebalance=false&destroy=false")

        self.assertEqual(200, response.status_code)

        api_url = "{}/docker/node/http://localhost:2345".format(tsuru_settings.TSURU_HOST)
        query = "?remove-iaas=false&no-rebalance=true"
        headers = {'authorization': u'admin'}
        delete.assert_called_with(api_url + query, headers=headers)

    @patch("requests.delete")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_remove_node_with_error(self, token_is_valid, delete):
        token_is_valid.return_value = True

        response_mock = Mock(status_code=404, text="custom error")
        delete.return_value = response_mock

        self.session["tsuru_token"] = "admin"
        self.session.save()

        url = reverse("node-remove", kwargs={"address": "http://localhost:2345"})
        response = self.client.delete(url, data="rebalance=true&destroy=true")

        self.assertEqual(404, response.status_code)
        self.assertEqual("custom error", response.content)

        api_url = "{}/docker/node/http://localhost:2345".format(tsuru_settings.TSURU_HOST)
        query = "?remove-iaas=true&no-rebalance=false"
        headers = {'authorization': u'admin'}
        delete.assert_called_with(api_url + query, headers=headers)

    @patch("requests.get")
    @patch("requests.delete")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_remove_node_with_rebalance_bad_request(self, token_is_valid, delete, get):
        token_is_valid.return_value = True

        response_mock = Mock(status_code=204)
        delete.return_value = response_mock

        self.session["tsuru_token"] = "admin"
        self.session.save()

        url = reverse("node-remove", kwargs={"address": "http://localhost:2345"})
        response = self.client.delete(url, data="rebalance=another&destroy=false")

        self.assertEqual(400, response.status_code)
        self.assertEqual("The value for 'rebalance' parameter should be 'true' or 'false'", response.content)

    @patch("requests.get")
    @patch("requests.delete")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_remove_node_with_destroy_bad_request(self, token_is_valid, delete, get):
        token_is_valid.return_value = True

        response_mock = Mock(status_code=204)
        delete.return_value = response_mock

        self.session["tsuru_token"] = "admin"
        self.session.save()

        url = reverse("node-remove", kwargs={"address": "http://localhost:2345"})
        response = self.client.delete(url, data="rebalance=true&destroy=another")

        self.assertEqual(400, response.status_code)
        self.assertEqual("The value for 'destroy' parameter should be 'true' or 'false'", response.content)
