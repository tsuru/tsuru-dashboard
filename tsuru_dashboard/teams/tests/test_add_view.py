from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from tsuru_dashboard import settings
from tsuru_dashboard.auth.views import LoginRequiredView
from tsuru_dashboard.teams.views import Add
from tsuru_dashboard.teams.forms import TeamForm


class TeamViewTest(TestCase):
    @patch("requests.get")
    def setUp(self, get):
        get.return_value = Mock(status_code=200)
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.session = {"tsuru_token": "admin"}
        self.response = Add.as_view()(self.request)
        self.request_post = self.factory.post('/team/', {'name': 'test-team'})
        self.request_post.session = {"tsuru_token": "admin"}

    def test_should_require_login_to_create_team(self):
        assert issubclass(Add, LoginRequiredView)

    def test_team_should_render_expected_template(self):
        self.assertEqual('auth/team.html', self.response.template_name)

    def test_context_should_contain_form(self):
        self.assertIn('form', self.response.context_data.keys())

    def test_form_in_context_should_has_a_instance_of_TeamForm(self):
        form = self.response.context_data.get('form')
        self.assertIsInstance(form, TeamForm)

    def test_get_request_team_url_should_not_return_404(self):
        response = self.client.get(reverse('team-add'))
        self.assertNotEqual(404, response.status_code)

    @patch('requests.post')
    @patch('requests.get')
    def test_post_sends_request_to_tsuru(self, get, post):
        get.return_value = Mock(status_code=200)
        self.request_post.session = {'tsuru_token': 'tokentest'}
        Add.as_view()(self.request_post)
        self.assertEqual(1, post.call_count)
        post.assert_called_with(
            '%s/teams' % settings.TSURU_HOST,
            data={"name": "test-team"},
            headers={'authorization':
                     self.request_post.session['tsuru_token']})

    @patch('requests.post')
    @patch('requests.get')
    def test_valid_post_redirect_to_team_list(self, get, post):
        get.return_value = Mock(status_code=200)
        post.return_value = Mock(status_code=200)
        response = Add.as_view()(self.request_post)
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse('team-list'), response.items()[1][1])

    @patch('requests.post')
    @patch('requests.get')
    def test_post_with_invalid_name_should_return_500(self, get, post):
        get.return_value = Mock(status_code=200)
        post.return_value = Mock(status_code=500, content='Error')
        response = Add.as_view()(self.request_post)
        self.assertEqual('Error', response.context_data.get('errors'))

    @patch("requests.get")
    def test_post_without_name_should_return_form_with_errors(self, get):
        get.return_value = Mock(status_code=200)
        request = self.factory.post('/team/', {'name': ''})
        request.session = {"tsuru_token": "admin"}
        response = Add.as_view()(request)
        form = response.context_data.get('form')
        self.assertIn('name', form.errors)
        self.assertIn(u'This field is required.', form.errors.get('name'))
