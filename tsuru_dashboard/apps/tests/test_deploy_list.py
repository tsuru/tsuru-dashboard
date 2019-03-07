from base64 import encodestring
from cStringIO import StringIO
from django.urls.base import reverse
from django.test import TestCase
from django.test.client import RequestFactory
from mock import patch, Mock
from zipfile import ZipFile

from tsuru_dashboard import settings
from tsuru_dashboard.apps.views import ListDeploy


@patch("tsuru_dashboard.auth.views.token_is_valid", return_value=True)
class ListDeployViewTest(TestCase):
    def setUp(self):
        self.app_name = 'my-awesome-app'
        kwargs = {'app_name': self.app_name}
        self.app_deploy_path = reverse('app-deploys', kwargs=kwargs)
        self.session = {'tsuru_token': 'just-another_tsuru_token'}
        self.get_request = RequestFactory().get(self.app_deploy_path, kwargs=kwargs)
        self.get_request.session = self.session

    @patch('requests.get')
    def test_context_should_contain_app(self, get, token_is_valid):
        response = ListDeploy.as_view()(self.get_request, app_name=self.app_name)
        self.assertIn('app', response.context_data.keys())

    @patch('requests.get')
    def test_should_use_deploys_template(self, get, token_is_valid):
        response = ListDeploy.as_view()(self.get_request, app_name=self.app_name)
        self.assertEqual("apps/deploys.html", response.template_name)
        self.assertIn('deploys', response.context_data.keys())

    @patch('requests.get')
    def test_deploy_list(self, get, token_is_valid):
        token_is_valid.return_value = True
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}

        view = ListDeploy
        view.get_app = Mock()
        self.response = view.as_view()(self.request, app_name="appname")

        url = '{}/deploys?app=appname&skip=0&limit=20'.format(settings.TSURU_HOST)
        headers = {'authorization': 'admin'}
        get.assert_called_with(url, headers=headers)

    @patch('requests.get')
    def test_empty_list(self, get, token_is_valid):
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = None
        get.return_value = response_mock
        token_is_valid.return_value = True

        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}

        view = ListDeploy
        view.get_app = Mock()
        view.as_view()(request, app_name="appname")

        url = '{}/deploys?app=appname&skip=0&limit=20'.format(settings.TSURU_HOST)
        headers = {'authorization': 'admin'}
        get.assert_called_with(url, headers=headers)

    def test_app_deploy_when_receives_invalid_params_should_return_400_with_expected_error_message(self, token_is_valid):
        test_cases = [
            {'request': RequestFactory().post(self.app_deploy_path, {})},
            {'request': RequestFactory().post(self.app_deploy_path, {'filecontent': 'this string was not encoded with base64'})}
        ]
        expected = {
            'status_code': 400,
            'content': 'the "filecontent" parameter is missing or it is not well formatted',
        }
        for test_case in test_cases:
            request = test_case.get('request')
            request.session = self.session
            response = ListDeploy.as_view()(request, app_name=self.app_name)
            error_message = 'Failure at test case: %s' % test_case
            self.assertEqual(expected.get('status_code'), response.status_code, error_message)
            self.assertEqual(expected.get('content'), response.content, error_message)

    @patch('requests.post')
    def test_app_deploy_when_receives_valid_parameters_should_deploy_on_api(self, post, token_is_valid):
        def generate_test_zip():
            zip_file_handler = StringIO()
            with ZipFile(zip_file_handler, mode='w') as zip_object:
                zip_object.writestr('hello.txt', 'Hello world :)')
            zip_file_handler.seek(0)
            return zip_file_handler
        zip_file_handler = generate_test_zip()
        encoded_file_content = encodestring(zip_file_handler.getvalue())
        targz_file_handler = ListDeploy.create_targz_file_object_from_zip_file(zip_file_handler)
        expected_content = targz_file_handler.getvalue()
        targz_file_handler.close()
        zip_file_handler.close()
        post.return_value = Mock(iter_lines=Mock(return_value=iter(['OK'])))
        request = RequestFactory().post(self.app_deploy_path, {'filecontent': encoded_file_content})
        request.session = self.session
        response = ListDeploy.as_view()(request, app_name=self.app_name)
        url = '{}/apps/{}/deploy?origin={}'.format(settings.TSURU_HOST, self.app_name, 'drag-and-drop')
        self.assertEqual(response.getvalue(), 'OK<br>')
        expected_headers = {'authorization': self.session.get('tsuru_token')}
        expected_files = {'file': ('archive.tar.gz', expected_content)}
        post.assert_called_with(url, headers=expected_headers, files=expected_files, stream=True)
