from mock import patch, Mock

from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from auth.views import LoginRequiredMixin, Key
from auth.forms import KeyForm


class KeyViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.session = {"tsuru_token": "admin"}
        self.response = Key.as_view()(self.request)
        self.request_post = self.factory.post('/team/', {'key': 'test-key-qq'})
        self.request_post.session = {"tsuru_token": "admin"}

    def test_should_require_login_to_create_team(self):
        assert issubclass(Key, LoginRequiredMixin)

    def test_key_should_render_expected_template(self):
        self.assertIn('auth/key.html', self.response.template_name)

    def test_context_should_contain_form(self):
        self.assertIn('form', self.response.context_data.keys())

    def test_form_in_context_should_has_a_instance_of_KeyForm(self):
        form = self.response.context_data.get('form')
        self.assertTrue(isinstance(form, KeyForm))

    def test_get_request_key_url_should_not_return_404(self):
        response = self.client.get(reverse('key'))
        self.assertNotEqual(404, response.status_code)

    @patch("django.contrib.messages.error")
    @patch('requests.post')
    def test_post_with_name_should_send_request_post_to_tsuru(self, post, er):
        self.request_post.session = {'tsuru_token': 'tokentest'}
        Key.as_view()(self.request_post)
        self.assertEqual(1, post.call_count)
        post.assert_called_with(
            '%s/users/keys' % settings.TSURU_HOST,
            data='{"key": "test-key-qq"}',
            headers={'authorization':
                     self.request_post.session['tsuru_token']})

    @patch("django.contrib.messages.success")
    @patch('requests.post')
    def test_valid_postshould_return_message_expected(self, post, success):
        post.return_value = Mock(status_code=200)
        Key.as_view()(self.request_post)
        success.assert_called_with(self.request_post, "The key was successfully added", fail_silently=True)

    @patch("django.contrib.messages.error")
    @patch('requests.post')
    def test_invalid_post_should_return_error_message(self, post, error):
        post.return_value = Mock(status_code=500, text='Error')
        Key.as_view()(self.request_post)
        error.assert_called_with(self.request_post, 'Error', fail_silently=True)

    @patch("django.contrib.messages.success")
    @patch('requests.post')
    def test_successfully_post_should_redirects(self, post, m):
        post.return_value = Mock(status_code=200)
        response = Key.as_view()(self.request_post)
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse('key'), response.items()[1][1])

    @patch("django.contrib.messages.error")
    @patch('requests.post')
    def test_post_with_error_should_redirects(self, post, er):
        post.return_value = Mock(status_code=500, content='Error')
        response = Key.as_view()(self.request_post)
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse('key'), response.items()[1][1])

    @patch('requests.post')
    def test_post_without_key_should_not_send_request_to_tsuru(self, post):
        request = self.factory.post('/team/', {'key': ''})
        request.session = {}
        Key.as_view()(request)
        self.assertEqual(0, post.call_count)

    @patch('requests.post')
    def test_post_without_key_should_return_form_with_errors(self, post):
        request = self.factory.post('/team/', {'key': ''})
        request.session = {"tsuru_token": "admin"}
        response = Key.as_view()(request)
        self.assertIn('form', response.context_data.keys())
        form = response.context_data.get('form')
        self.assertTrue(isinstance(form, KeyForm))
        self.assertEqual(u'This field is required.',
                         form.errors.get('key')[0])
