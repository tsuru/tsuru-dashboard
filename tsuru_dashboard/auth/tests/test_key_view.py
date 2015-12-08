from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from tsuru_dashboard import settings
from tsuru_dashboard.auth.views import LoginRequiredMixin, KeyAdd
from tsuru_dashboard.auth.forms import KeyForm


class KeyViewTest(TestCase):
    @patch("requests.get")
    def setUp(self, get):
        get.return_value = Mock(status_code=200)
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.session = {"tsuru_token": "admin"}
        self.response = KeyAdd.as_view()(self.request)
        self.request_post = self.factory.post('/key/', {'key': 'test-key-qq', 'name': 'mykey'})
        self.request_post.session = {"tsuru_token": "admin"}

    def test_should_require_login_to_create_team(self):
        assert issubclass(KeyAdd, LoginRequiredMixin)

    def test_key_should_render_expected_template(self):
        self.assertIn('auth/key_add.html', self.response.template_name)

    def test_context_should_contain_form(self):
        self.assertIn('form', self.response.context_data.keys())

    def test_form_in_context_should_has_a_instance_of_KeyForm(self):
        form = self.response.context_data.get('form')
        self.assertIsInstance(form, KeyForm)

    def test_get_request_key_url_should_not_return_404(self):
        response = self.client.get(reverse('key'))
        self.assertNotEqual(404, response.status_code)

    @patch("django.contrib.messages.error")
    @patch('requests.post')
    @patch('requests.get')
    def test_post_with_name_should_send_request_post_to_tsuru(self, get, post, er):
        get.return_value = Mock(status_code=200)
        self.request_post.session = {'tsuru_token': 'tokentest'}
        KeyAdd.as_view()(self.request_post)
        self.assertEqual(1, post.call_count)
        post.assert_called_with(
            '%s/users/keys' % settings.TSURU_HOST,
            data='{"name": "mykey", "key": "test-key-qq"}',
            headers={'authorization':
                     self.request_post.session['tsuru_token']})

    @patch("django.contrib.messages.success")
    @patch('requests.post')
    @patch('requests.get')
    def test_valid_postshould_return_message_expected(self, get, post, success):
        get.return_value = Mock(status_code=200)
        post.return_value = Mock(status_code=200)
        KeyAdd.as_view()(self.request_post)
        success.assert_called_with(self.request_post, "The key was successfully added", fail_silently=True)

    @patch("django.contrib.messages.error")
    @patch('requests.post')
    @patch('requests.get')
    def test_invalid_post_should_return_error_message(self, get, post, error):
        get.return_value = Mock(status_code=200)
        post.return_value = Mock(status_code=500, text='Error')
        KeyAdd.as_view()(self.request_post)
        error.assert_called_with(self.request_post, 'Error', fail_silently=True)

    @patch("django.contrib.messages.success")
    @patch('requests.post')
    @patch('requests.get')
    def test_successfully_post_should_redirects(self, get, post, m):
        get.return_value = Mock(status_code=200)
        post.return_value = Mock(status_code=200)
        response = KeyAdd.as_view()(self.request_post)
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse('key'), response.items()[1][1])

    @patch("django.contrib.messages.error")
    @patch('requests.post')
    @patch('requests.get')
    def test_post_with_error_should_redirects(self, get, post, er):
        get.return_value = Mock(status_code=200)
        post.return_value = Mock(status_code=500, content='Error')
        response = KeyAdd.as_view()(self.request_post)
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse('key'), response.items()[1][1])

    @patch('requests.post')
    @patch('requests.get')
    def test_post_without_key_should_not_send_request_to_tsuru(self, get, post):
        get.return_value = Mock(status_code=200)
        request = self.factory.post('/team/', {'key': ''})
        request.session = {}
        KeyAdd.as_view()(request)
        self.assertEqual(0, post.call_count)

    @patch('requests.post')
    @patch('requests.get')
    def test_post_without_key_should_return_form_with_errors(self, get, post):
        get.return_value = Mock(status_code=200)
        request = self.factory.post('/team/', {'key': ''})
        request.session = {"tsuru_token": "admin"}
        response = KeyAdd.as_view()(request)
        self.assertIn('form', response.context_data.keys())
        form = response.context_data.get('form')
        self.assertIsInstance(form, KeyForm)
        self.assertEqual(u'This field is required.',
                         form.errors.get('key')[0])
