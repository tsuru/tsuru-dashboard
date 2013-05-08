from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory
from django.conf import settings

from services.views import ServiceInstanceDetail


class ServiceInstanceDetailViewTest(TestCase):
    @patch("requests.get")
    def test_view(self, get):
        data = {u'Name': u'instance'}
        response_mock = Mock()
        response_mock.json.return_value = data
        get.return_value = response_mock
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}
        response = ServiceInstanceDetail.as_view()(request,
                                                   instance="instance")
        self.assertEqual("services/detail.html", response.template_name)
        self.assertDictEqual({u"Name": "instance"},
                             response.context_data['instance'])
        get.assert_called_with(
            '{0}/services/instances/{1}'.format(settings.TSURU_HOST,
                                                "instance"),
            headers={'authorization': 'admin'})
