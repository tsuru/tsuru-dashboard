from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory

from tsuru_dashboard import settings
from tsuru_dashboard.services.views import ServiceInstanceDetail


class ServiceInstanceDetailViewTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}

    @patch("tsuru_dashboard.services.views.ServiceInstanceDetail.apps")
    @patch("requests.get")
    def test_get_instance_data(self, get, apps):
        data = {u'Name': u'instance', u'Tags': [u'tag1', u'tag2']}
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = data
        get.return_value = response_mock

        response = ServiceInstanceDetail.as_view()(self.request, service="service",
                                                   instance="instance")

        self.assertIn("services/detail.html", response.template_name)
        self.assertDictEqual({u'Name': u'instance', u'Tags': u'tag1, tag2'}, response.context_data['instance'])
        url = '{}/services/{}/instances/{}'.format(settings.TSURU_HOST, "service", "instance")
        get.assert_called_with(url, headers={'authorization': 'admin'})

    @patch("tsuru_dashboard.services.views.ServiceInstanceDetail.apps")
    @patch("requests.get")
    def test_get_instance_data_no_tags(self, get, apps):
        data = {u'Name': u'instance', u'Tags': ''}
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = data
        get.return_value = response_mock

        response = ServiceInstanceDetail.as_view()(self.request, service="service",
                                                   instance="instance")

        self.assertIn("services/detail.html", response.template_name)
        # Empty string
        self.assertDictEqual({u'Name': u'instance', u'Tags': u''}, response.context_data['instance'])
        url = '{}/services/{}/instances/{}'.format(settings.TSURU_HOST, "service", "instance")
        get.assert_called_with(url, headers={'authorization': 'admin'})

        # Empty array
        data = {u'Name': u'instance', u'Tags': []}
        response_mock.json.return_value = data
        get.return_value = response_mock
        response = ServiceInstanceDetail.as_view()(self.request, service="service",
                                                   instance="instance")
        self.assertDictEqual({u'Name': u'instance', u'Tags': u''}, response.context_data['instance'])

        # None
        data = {u'Name': u'instance', u'Tags': None}
        response_mock.json.return_value = data
        get.return_value = response_mock
        response = ServiceInstanceDetail.as_view()(self.request, service="service",
                                                   instance="instance")
        self.assertDictEqual({u'Name': u'instance', u'Tags': u''}, response.context_data['instance'])

    @patch("tsuru_dashboard.services.views.ServiceInstanceDetail.get_instance")
    @patch("requests.get")
    def test_get_apps(self, get, get_instance):
        instance_mock = {'Apps': ["ble"]}
        get_instance.return_value = instance_mock
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = [
            {u'name': u'app1'},
            {u'name': u'ble'},
            {u'name': u'app2'}
        ]
        get.return_value = response_mock

        response = ServiceInstanceDetail.as_view()(self.request, service="service",
                                                   instance="instance")

        self.assertIn("services/detail.html", response.template_name)
        self.assertIn("apps", response.context_data)
        expected = ["app1", "app2"]
        self.assertListEqual(expected, response.context_data["apps"])
        url = '{}/apps'.format(settings.TSURU_HOST)
        get.assert_called_with(url, headers={'authorization': 'admin'})
