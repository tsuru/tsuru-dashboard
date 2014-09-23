from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory
from django.conf import settings

from admin.views import ListContainersByApp


class ListContainerViewTest(TestCase):
    @patch("requests.get")
    def setUp(self, get):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.session = {'tsuru_token': 'tokentest'}
        self.appname = 'myapp'
        self.response_mock = Mock()
        self.response_mock.status_code = 200
        self.response_mock.content = '{}'
        self.response = ListContainersByApp().get(self.request, self.appname)

    @patch('requests.get')
    def test_request_get_to_tsuru_with_args_expected(self, get):
        ListContainersByApp().get(self.request, self.appname)
        get.assert_called_with(
            '%s/docker/node/apps/%s/containers' % (settings.TSURU_HOST,
                                                   self.appname),
            headers={'authorization': self.request.session['tsuru_token']})

    @patch('requests.get')
    def test_should_use_list_template(self, get):
        get.return_value = Mock(status_code=204)
        response = ListContainersByApp.as_view()(self.request, self.appname)
        self.assertEqual("apps/list_containers.html", response.template_name)
        self.assertListEqual([], response.context_data['containers'])

    @patch('requests.get')
    def teste_should_get_list_of_containers_from_tsuru(self, get):
        expected = [{"id": "blabla", "type": "python",
                     "appname": "myapp",
                     "hostaddr": "http://cittavld1182.globoi.com"}]
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = expected
        get.return_value = response_mock
        response = ListContainersByApp.as_view()(self.request, self.appname)
        self.assertListEqual([{"id": "blabla", "type": "python",
                               "appname": "myapp",
                               "hostaddr": "http://cittavld1182.globoi.com"}],
                             response.context_data["containers"])
