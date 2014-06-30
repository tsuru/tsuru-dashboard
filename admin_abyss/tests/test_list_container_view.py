from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.conf import settings

from admin_abyss.views import ListContainer


class ListContainerViewTest(TestCase):
    @patch("requests.get")
    def setUp(self, get):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.session = {'tsuru_token': 'tokentest'}
        self.address = 'http://cittavld1182.globoi.com'
        self.response_mock = Mock()
        self.response_mock.status_code = 200
        self.response_mock.content = '{}'
        self.response = ListContainer().get(self.request, self.address)

    @patch('requests.get')
    def test_request_get_to_tsuru_with_args_expected(self, get):
        ListContainer().get(self.request, self.address)
        get.assert_called_with(
            '%s/docker/node/%s/containers' % (settings.TSURU_HOST,
                                              self.address),
            headers={'authorization': self.request.session['tsuru_token']})

    @patch('requests.get')
    def teste_should_get_list_of_containers_from_tsuru(self, get):
        expected = [{"id": "blabla", "type": "python",
                     "appname": "myapp",
                     "hostaddr": "http://cittavld1182.globoi.com"}]
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = expected
        get.return_value = response_mock
        response = ListContainer.as_view()(self.request, self.address)
        self.assertListEqual([{"id": "blabla", "type": "python",
                               "appname": "myapp",
                               "hostaddr": "http://cittavld1182.globoi.com"}],
                             response.context_data["containers"])

    def test_get_request_run_url_should_not_return_404(self):
        response = self.client.get(reverse('list-container',
                                   args=[self.address.replace("http://", "")]))
        self.assertNotEqual(404, response.status_code)
