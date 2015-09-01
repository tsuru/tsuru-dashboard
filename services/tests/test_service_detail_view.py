from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory
from django.conf import settings

from services.views import ServiceInstanceDetail


class ServiceInstanceDetailViewTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}

    @patch("services.views.ServiceInstanceDetail.apps")
    @patch("requests.get")
    def test_get_instance_data(self, get, apps):
        data = {u'Name': u'instance'}
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = data
        get.return_value = response_mock
        response = ServiceInstanceDetail.as_view()(self.request,
                                                   instance="instance")
        self.assertIn("services/detail.html", response.template_name)
        self.assertDictEqual({u"Name": "instance"},
                             response.context_data['instance'])
        get.assert_called_with(
            '{0}/services/instances/{1}'.format(settings.TSURU_HOST,
                                                "instance"),
            headers={'authorization': 'admin'})

    @patch("services.views.ServiceInstanceDetail.get_instance")
    @patch("requests.get")
    def test_get_apps(self, get, get_instance):
        instance_mock = {'Apps': ["ble"]}
        get_instance.return_value = instance_mock
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = [{u'name': u'app1'},
                                           {u'name': u'ble'},
                                           {u'name': u'app2'}]
        get.return_value = response_mock
        response = ServiceInstanceDetail.as_view()(self.request,
                                                   instance="instance")
        self.assertIn("services/detail.html", response.template_name)
        self.assertIn("apps", response.context_data)
        expected = ["app1", "app2"]
        self.assertListEqual(expected, response.context_data["apps"])
        get.assert_called_with('{0}/apps'.format(settings.TSURU_HOST),
                               headers={'authorization': 'admin'})
