from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.conf import settings

from admin.views import NodeInfo


class NodeInfoViewTest(TestCase):
    @patch("requests.get")
    def setUp(self, get):
        get.return_value = Mock(status_code=200)
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.session = {'tsuru_token': 'tokentest'}
        self.address = 'cittavld1182.globoi.com'
        self.response_mock = Mock()
        self.response_mock.status_code = 200
        self.response_mock.content = '{}'
        self.response = NodeInfo.as_view()(self.request, address=self.address)

    @patch('requests.get')
    def test_request_get_to_tsuru_with_args_expected(self, get):
        get.return_value = Mock(status_code=200)
        NodeInfo.as_view()(self.request, address=self.address)
        url = "{}/docker/node/{}/containers".format(settings.TSURU_HOST, self.address)
        get.assert_called_with(
            url,
            headers={'authorization': self.request.session['tsuru_token']})

    @patch('requests.get')
    @patch("auth.views.token_is_valid")
    def test_should_use_list_template(self, token_is_valid, get):
        token_is_valid.return_value = True
        get.return_value = Mock(status_code=204)
        response = NodeInfo.as_view()(self.request, address=self.address)
        self.assertIn("admin/node_info.html", response.template_name)
        self.assertListEqual([], response.context_data['containers'])

    @patch('requests.get')
    def teste_should_get_list_of_containers_from_tsuru(self, get):
        get.return_value = Mock(status_code=200)
        expected = [{"id": "blabla", "type": "python",
                     "appname": "myapp",
                     "hostaddr": "http://cittavld1182.globoi.com"}]
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = expected
        get.return_value = response_mock
        response = NodeInfo.as_view()(self.request, address=self.address)
        self.assertListEqual(expected, response.context_data["containers"])

    def test_get_request_run_url_should_not_return_404(self):
        response = self.client.get(reverse('node-info',
                                   args=[self.address.replace("http://", "")]))
        self.assertNotEqual(404, response.status_code)
