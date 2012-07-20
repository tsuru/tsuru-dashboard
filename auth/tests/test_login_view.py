from django.conf import settings
from django.http import HttpResponseRedirect
from django.test import TestCase
from django.test.client import RequestFactory
from mock import Mock, patch

from auth.forms import LoginForm
from auth.views import Login


class LoginViewTest(TestCase):
    def test_root_should_show_login_template(self):
        request = RequestFactory().get('/')
        response = Login().get(request)
        self.assertEqual('auth/login.html', response.template_name)

    def test_login_should_show_template(self):
        request = RequestFactory().get('/login')
        response = Login().get(request)
        self.assertEqual('auth/login.html', response.template_name)

    def test_login_form_should_be_in_the_view_context(self):
        request = RequestFactory().get('/')
        response = Login().get(request)
        form = response.context_data['login_form']
        self.assertIsInstance(form, LoginForm)

    def test_should_validate_data_from_post(self):
        data = {'username': 'invalid name', 'password': ''}
        request = RequestFactory().post('/', data)
        response = Login().post(request)
        form = response.context_data['login_form']

        self.assertEqual('auth/login.html', response.template_name)
        self.assertIsInstance(form, LoginForm)
        self.assertEqual('invalid name', form.data['username'])

    def test_should_return_200_when_user_does_not_exist(self):
        data = {'username': 'invalid@email.com', 'password': '123456'}
        request = RequestFactory().post('/', data)

        with patch('requests.post') as post:
            response_mock = Mock()
            response_mock.status_code = 500
            post.side_effect = Mock(return_value=response_mock)
            response = Login().post(request)
            self.assertEqual(200, response.status_code)
            self.assertEqual('auth/login.html', response.template_name)
            error_msg = response.context_data['msg']
            self.assertEqual('User not found', error_msg)

    def test_should_send_request_post_to_tsuru_with_args_expected(self):
        data = {'username': 'valid@email.com', 'password': '123456'}
        request = RequestFactory().post('/', data)
        expected_url = '%s/users/valid@email.com/tokens' % settings.TSURU_HOST

        with patch('requests.post') as post:
            Login().post(request)
            self.assertEqual(1, post.call_count)
            post.assert_called_with(expected_url, data='{"password": "123456"}')

    def test_should_set_token_in_the_session(self):
        data = {'username': 'valid@email.com', 'password': '123456'}
        request = RequestFactory().post('/', data)
        request.session = {}

        with patch('requests.post') as post:
            response_mock = Mock()
            response_mock.status_code = 200
            response_mock.text = '{"token": "my beautiful token"}'
            post.side_effect = Mock(return_value=response_mock)
            Login().post(request)
            self.assertEqual('my beautiful token', request.session["tsuru_token"])

    def test_redirect_to_team_creation_page_when_login_is_successful(self):
        data = {'username': 'valid@email.com', 'password': '123456'}
        request = RequestFactory().post('/', data)
        request.session = {}

        with patch('requests.post') as post:
            response_mock = Mock()
            response_mock.status_code = 200
            response_mock.text = '{"token": "my beautiful token"}'
            post.side_effect = Mock(return_value=response_mock)
            response = Login().post(request)
            self.assertIsInstance(response, HttpResponseRedirect)
            self.assertEqual('/team', response['Location'])
