from django.test import TestCase
from django.test.client import RequestFactory
from mock import Mock, patch

from tsuru_dashboard import settings
from tsuru_dashboard.auth.forms import SignupForm
from tsuru_dashboard.auth.views import Signup


class SignupViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.response = Signup().get(self.request)
        self.response_mock = Mock()

    def test_signup_should_show_template(self):
        self.assertEqual('auth/signup.html', self.response.template_name)

    def test_context_should_contain_form(self):
        form = self.response.context_data['signup_form']
        self.assertIsInstance(form, SignupForm)

    def test_should_validate_data_from_post(self):
        data = {'email': '', 'password': '', 'same_password_again': ''}
        request = self.factory.post('/signup', data)
        response = Signup().post(request)
        form = response.context_data['signup_form']
        self.assertIn(u'This field is required.', form.errors['email'])
        self.assertIn(u'This field is required.', form.errors['password'])
        self.assertIn(u'This field is required.',
                      form.errors['same_password_again'])

    @patch('requests.post')
    @patch('requests.get')
    def test_return_msg_on_success(self, get, post):
        get.return_value = Mock(status_code=200)
        data = {'email': 'test@test.com', 'password': 'abc123',
                'same_password_again': 'abc123'}
        request = self.factory.post('/signup', data)
        post.return_value = Mock(status_code=201)
        response = Signup.as_view()(request)
        expected = 'User "{0}" successfully created!'.format(data["email"])
        self.assertEqual(expected, response.context_data["message"])

    @patch('requests.post')
    @patch('requests.get')
    def test_post_sends_to_tsuru_with_args_expected(self, get, post):
        get.return_value = Mock(status_code=200)
        data = {'email': 'test@test.com', 'password': 'abc123',
                'same_password_again': 'abc123'}
        request = self.factory.post('/signup', data)
        Signup().post(request)
        self.assertEqual(1, post.call_count)
        post.assert_called_with(
            '%s/users' % settings.TSURU_HOST,
            data='{"password": "abc123", "email": "test@test.com"}')
