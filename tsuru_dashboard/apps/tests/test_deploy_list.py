from mock import patch, Mock
from base64 import encodestring
import os.path
import subprocess

from django.test import TestCase
from django.test.client import RequestFactory

from tsuru_dashboard import settings
from tsuru_dashboard.apps.views import ListDeploy


class ListDeployViewTest(TestCase):
    @patch('requests.get')
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def setUp(self, token_is_valid, get):
        token_is_valid.return_value = True
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}
        self.response = ListDeploy.as_view()(self.request, app_name="appname")

    def test_context_should_contain_app(self):
        self.assertIn('app', self.response.context_data.keys())

    @patch('requests.get')
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_should_use_deploys_template(self, token_is_valid, get):
        token_is_valid.return_value = True
        get.return_value = Mock(status_code=200)
        self.assertEqual("apps/deploys.html", self.response.template_name)
        self.assertIn('deploys', self.response.context_data.keys())

    @patch('requests.get')
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_deploy_list(self, token_is_valid, get):
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
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_empty_list(self, token_is_valid, get):
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

    @patch('requests.post')
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_targz(self, token_is_valid, post):
        response_mock = Mock(status_code=200)
        response_mock.iter_lines.return_value = iter(["expected"])

        post.return_value = response_mock

        token_is_valid.return_value = True

        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        zip_file = open(os.path.join(BASE_DIR, "example.zip"))
        encoded = encodestring(zip_file.read())

        request = RequestFactory().post("/", {"filecontent": encoded})
        request.session = {"tsuru_token": "admin"}
        tar_path = os.path.join(BASE_DIR, "example.tar.gz")

        def deploy(self, request, app_name, content):
            tar_file = open(tar_path, "wb")
            tar_file.write(content.getvalue())
            tar_file.close()

        view = ListDeploy
        view.deploy = deploy
        view.as_view()(request, app_name="appname")

        cmd = ["tar", "zxvf", "{}".format(tar_path), "-C", "/tmp"]
        pipes = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, stderr = pipes.communicate()

        self.assertEqual(pipes.returncode, 0)
        self.assertNotIn("Damaged", stderr)
