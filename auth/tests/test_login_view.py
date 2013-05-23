from django.conf import settings
from django.http import HttpResponseRedirect
from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from mock import Mock, patch

from auth.forms import LoginForm
from auth.views import Login

from intro.models import Intro


class LoginViewTest(TestCase):
    def test_login_get(self):
        request = RequestFactory().get('/')
        response = Login.as_view()(request)
        self.assertIn('auth/login.html', response.template_name)
        form = response.context_data['form']
        self.assertIsInstance(form, LoginForm)

    def test_should_validate_data_from_post(self):
        data = {'username': 'invalid name', 'password': ''}
        request = RequestFactory().post('/', data)
        response = Login.as_view()(request)
        form = response.context_data['form']
        self.assertIn('auth/login.html', response.template_name)
        self.assertIsInstance(form, LoginForm)
        self.assertEqual('invalid name', form.data['username'])

    @patch('requests.post')
    def test_should_return_200_when_user_does_not_exist(self, post):
        data = {'username': 'invalid@email.com', 'password': '123456'}
        post.return_value = Mock(status_code=500)
        response = self.client.post(reverse('login'), data, follow=True)
        self.assertRedirects(response, reverse('login'))

    @patch('requests.post')
    def test_should_send_request_post_to_tsuru_with_args_expected(self, post):
        data = {'username': 'valid@email.com', 'password': '123456'}
        request = RequestFactory().post('/', data)
        expected_url = '%s/users/valid@email.com/tokens' % settings.TSURU_HOST
        Login.as_view()(request)
        self.assertEqual(1, post.call_count)
        post.assert_called_with(expected_url,
                                data='{"password": "123456"}')

    @patch('requests.post')
    def test_should_set_token_in_the_session(self, post):
        data = {'username': 'valid@email.com', 'password': '123456'}
        request = RequestFactory().post('/', data)
        request.session = {}
        text = '{"token": "my beautiful token"}'
        post.return_value = Mock(status_code=200, text=text)
        Login.as_view()(request)
        self.assertEqual('type my beautiful token',
                         request.session["tsuru_token"])

    @patch('requests.post')
    def test_should_set_username_in_the_session(self, post):
        post.return_value = Mock(status_code=200,
                                 text='{"token": "t"}')
        data = {'username': 'valid@email.com', 'password': '123456'}
        request = RequestFactory().post('/', data)
        request.session = {}
        Login.as_view()(request)
        self.assertEqual(data["username"], request.session["username"])

    @patch('requests.post')
    @override_settings(INTRO_ENABLED=False)
    def test_redirect_to_team_creation_when_login_is_successful(self, post):
        data = {'username': 'valid@email.com', 'password': '123456'}
        request = RequestFactory().post('/', data)
        request.session = {}
        text = '{"token": "my beautiful token"}'
        post.return_value = Mock(status_code=200, text=text)
        response = Login.as_view()(request)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual('/apps', response['Location'])

    @patch('requests.post')
    @override_settings(INTRO_ENABLED=False)
    def test_redirect_to_team_creation_settings_false(self, post):
        data = {'username': 'valid@email.com', 'password': '123456'}
        request = RequestFactory().post('/', data)
        request.session = {}
        text = '{"token": "my beautiful token"}'
        post.return_value = Mock(status_code=200, text=text)
        response = Login.as_view()(request)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual('/apps', response['Location'])

    @patch('requests.post')
    @override_settings(INTRO_ENABLED=True)
    def test_redirect_to_team_creation_settings_true(self, post):
        data = {'username': 'valid@email.com', 'password': '123456'}
        request = RequestFactory().post('/intro', data)
        request.session = {}
        text = '{"token": "my beautiful token"}'
        post.return_value = Mock(status_code=200, text=text)
        response = Login.as_view()(request)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual('/intro', response['Location'])
        response = Login.as_view()(request)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual('/apps', response['Location'])
        Intro.objects.filter(email=data['username']).delete()

    @patch('requests.post')
    @override_settings(INTRO_ENABLED=True)
    def test_redirect_to_apps_when_the_intro_alread_exist(self, post):
        data = {'username': 'valid@email.com', 'password': '123456'}
        intro = Intro.objects.create(email=data['username'])
        request = RequestFactory().post('/', data)
        request.session = {}
        text = '{"token": "my beautiful token"}'
        post.return_value = Mock(status_code=200, text=text)
        response = Login.as_view()(request)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual('/apps', response['Location'])
        intro.delete()
