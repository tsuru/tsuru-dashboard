from django.test import TestCase
from django.test.client import RequestFactory
from django.http import Http404

from tsuru_dashboard import settings
from tsuru_dashboard.apps.views import AppDetailJson

from mock import patch

import json
import httpretty


class AppDetailJsonTestCase(TestCase):
    def setUp(self):
        self.maxDiff = None
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}
        self.request = request

    @httpretty.activate
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_view(self, token_is_valid):
        token_is_valid.return_value = True

        url = '{}/docker/node/apps/{}/containers'.format(settings.TSURU_HOST, "app1")
        body = json.dumps([])
        httpretty.register_uri(httpretty.GET, url, body=body, status=200)

        data = {
            "name": "app1",
            "framework": "php",
            "repository": "git@git.com:php.git",
            "state": "dead",
            "units": [
                {"Ip": "10.10.10.10", "Status": "started", "ProcessName": "web", "Name": "xpto"},
                {"Ip": "9.9.9.9", "Status": "stopped", "ProcessName": "worker", "Name": "unitx"},
            ],
            "teams": ["tsuruteam", "crane"]
        }

        url = '{}/apps/{}'.format(settings.TSURU_HOST, "app1")
        body = json.dumps(data)
        httpretty.register_uri(httpretty.GET, url, body=body, status=200)

        response = AppDetailJson.as_view()(self.request, app_name="app1")

        expected = {
            u'app': {
                u'name': u'app1',
                u'repository': u'git@git.com:php.git',
                u'teams': [u'tsuruteam', u'crane'],
                u'framework': u'php',
                u'state': u'dead',
                u'units': [
                    {u'Status': u'started', u'Ip': u'10.10.10.10', u'Name': u'xpto', u'ProcessName': u'web'},
                    {u'Status': u'stopped', u'Ip': u'9.9.9.9', u'Name': u'unitx', u'ProcessName': u'worker'}
                ]
            },
            u'process_list': [u'web', u'worker'],
            u'units_by_status': {
                u'started': [
                    {u'Status': u'started', u'Ip': u'10.10.10.10', u'Name': u'xpto', u'ProcessName': u'web'}
                ],
                u'stopped': [
                    {u'Status': u'stopped', u'Ip': u'9.9.9.9', u'Name': u'unitx', u'ProcessName': u'worker'}
                ]
            }
        }
        self.assertDictEqual(expected, json.loads(response.content))

    @httpretty.activate
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_not_found(self, token_is_valid):
        token_is_valid.return_value = True

        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}

        url = '{}/apps/{}'.format(settings.TSURU_HOST, "app1")
        httpretty.register_uri(httpretty.GET, url, status=404)

        with self.assertRaises(Http404):
            AppDetailJson.as_view()(request, app_name="app1")

    @httpretty.activate
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_view_get_contaienrs_not_200(self, token_is_valid):
        token_is_valid.return_value = True

        url = '{}/docker/node/apps/{}/containers'.format(settings.TSURU_HOST, "app1")
        httpretty.register_uri(httpretty.GET, url, status=403)

        data = {
            "name": "app1",
            "framework": "php",
            "repository": "git@git.com:php.git",
            "state": "dead",
            "units": [
                {"Ip": "10.10.10.10", "Status": "started", "ProcessName": "web", "Name": "xpto"},
                {"Ip": "9.9.9.9", "Status": "stopped", "ProcessName": "worker", "Name": "unitx"},
            ],
            "teams": ["tsuruteam", "crane"]
        }

        url = '{}/apps/{}'.format(settings.TSURU_HOST, "app1")
        body = json.dumps(data)
        httpretty.register_uri(httpretty.GET, url, body=body, status=200)

        response = AppDetailJson.as_view()(self.request, app_name="app1")

        expected = {
            u'app': {
                u'name': u'app1',
                u'repository': u'git@git.com:php.git',
                u'teams': [u'tsuruteam', u'crane'],
                u'framework': u'php',
                u'state': u'dead',
                u'units': [
                    {u'Status': u'started', u'Ip': u'10.10.10.10', u'Name': u'xpto', u'ProcessName': u'web'},
                    {u'Status': u'stopped', u'Ip': u'9.9.9.9', u'Name': u'unitx', u'ProcessName': u'worker'}
                ]
            },
            u'process_list': [u'web', u'worker'],
            u'units_by_status': {
                u'started': [
                    {u'Status': u'started', u'Ip': u'10.10.10.10', u'Name': u'xpto', u'ProcessName': u'web'}
                ],
                u'stopped': [
                    {u'Status': u'stopped', u'Ip': u'9.9.9.9', u'Name': u'unitx', u'ProcessName': u'worker'}
                ]
            }
        }
        self.assertDictEqual(expected, json.loads(response.content))
