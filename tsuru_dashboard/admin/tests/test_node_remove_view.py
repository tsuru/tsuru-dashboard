from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings

from importlib import import_module

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

        response_mock = Mock(status_code=204)
        delete.return_value = response_mock

        self.session["tsuru_token"] = "admin"
        self.session.save()

        response = self.client.get(
            reverse("node-remove", kwargs={"address": "http://localhost:2345"}))

        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse("pool-list"))

        api_url = "http://localhost:8080/docker/node?no-rebalance=true"
        headers = {'authorization': u'admin'}
        data = '{"remove_iaas": "false", "address": "http://localhost:2345"}'
        delete.assert_called_with(api_url, headers=headers, data=data)

    @patch("requests.get")
    @patch("requests.delete")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_remove_node_with_detroy_and_rebalance_true(self, token_is_valid, delete, get):
        token_is_valid.return_value = True

        response_mock = Mock(status_code=204)
        delete.return_value = response_mock

        self.session["tsuru_token"] = "admin"
        self.session.save()

        url = "{}?rebalance=true&destroy=true".format(
            reverse("node-remove", kwargs={"address": "http://localhost:2345"}))
        response = self.client.get(url)

        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse("pool-list"))

        api_url = "http://localhost:8080/docker/node?no-rebalance=false"
        headers = {'authorization': u'admin'}
        data = '{"remove_iaas": "true", "address": "http://localhost:2345"}'
        delete.assert_called_with(api_url, headers=headers, data=data)

    @patch("requests.get")
    @patch("requests.delete")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_remove_node_with_detroy_and_rebalance_false(self, token_is_valid, delete, get):
        token_is_valid.return_value = True

        response_mock = Mock(status_code=204)
        delete.return_value = response_mock

        self.session["tsuru_token"] = "admin"
        self.session.save()

        url = "{}?rebalance=false&destroy=false".format(
            reverse("node-remove", kwargs={"address": "http://localhost:2345"}))
        response = self.client.get(url)

        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse("pool-list"))

        api_url = "http://localhost:8080/docker/node?no-rebalance=true"
        headers = {'authorization': u'admin'}
        data = '{"remove_iaas": "false", "address": "http://localhost:2345"}'
        delete.assert_called_with(api_url, headers=headers, data=data)

    @patch("requests.delete")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_remove_node_with_error(self, token_is_valid, delete):
        token_is_valid.return_value = True

        response_mock = Mock(status_code=404, text="custom error")
        delete.return_value = response_mock

        self.session["tsuru_token"] = "admin"
        self.session.save()

        url = "{}?rebalance=true&destroy=true".format(
            reverse("node-remove", kwargs={"address": "http://localhost:2345"}))
        response = self.client.get(url)

        self.assertEqual(404, response.status_code)
        self.assertEqual("custom error", response.content)

        api_url = "http://localhost:8080/docker/node?no-rebalance=false"
        headers = {'authorization': u'admin'}
        data = '{"remove_iaas": "true", "address": "http://localhost:2345"}'
        delete.assert_called_with(api_url, headers=headers, data=data)

    @patch("requests.get")
    @patch("requests.delete")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_remove_node_with_rebalance_bad_request(self, token_is_valid, delete, get):
        token_is_valid.return_value = True

        response_mock = Mock(status_code=204)
        delete.return_value = response_mock

        self.session["tsuru_token"] = "admin"
        self.session.save()

        url = "{}?rebalance=another&destroy=false".format(
            reverse("node-remove", kwargs={"address": "http://localhost:2345"}))
        response = self.client.get(url)

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

        url = "{}?rebalance=true&destroy=another".format(
            reverse("node-remove", kwargs={"address": "http://localhost:2345"}))
        response = self.client.get(url)

        self.assertEqual(400, response.status_code)
        self.assertEqual("The value for 'destroy' parameter should be 'true' or 'false'", response.content)
