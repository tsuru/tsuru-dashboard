from tempfile import TemporaryFile

from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.test.client import RequestFactory

from mock import patch

from apps.views import DeployUpload


class DeployUploadTest(TestCase):

    def test_mapped_url(self):
        expect_URL = '/apps/test_app/deploy/upload'
        url = reverse('app-deploy-upload', kwargs={'app_name': 'test_app'})
        self.assertEqual(url, expect_URL)

        view = resolve(expect_URL)
        self.assertEqual(view.url_name, 'app-deploy-upload')

    @patch('auth.views.token_is_valid')
    def test_need_fail_if_there_is_no_file(self, mck_token_is_valid):
        url = reverse('app-deploy-upload', kwargs={'app_name': 'test_app'})
        request = RequestFactory().post(url)
        request.session = {'tsuru_token': 'admin'}
        response = DeployUpload.as_view()(request)

        self.assertEqual(response.status_code, 500)
        self.assertIn('no file found', response.content)

    @patch('auth.views.token_is_valid')
    def test_if_found_the_file(self, mck_token_is_valid):
        url = reverse('app-deploy-upload', kwargs={'app_name': 'test_app'})
        tempfile = TemporaryFile()
        tempfile.write('foo')
        tempfile.seek(0)
        with tempfile as fd:
            request = RequestFactory().post(url, {'files': fd})
            request.session = {'tsuru_token': 'admin'}
            response = DeployUpload.as_view()(request)
            self.assertEqual(response.status_code, 200)
