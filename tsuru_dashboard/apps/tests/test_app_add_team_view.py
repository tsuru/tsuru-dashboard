import json

from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from tsuru_dashboard import settings
from tsuru_dashboard.apps.views import AppAddTeam
from tsuru_dashboard.auth.views import LoginRequiredView
from tsuru_dashboard.apps.forms import AppAddTeamForm


class AppAddTeamTestCase(TestCase):
    @patch('requests.get')
    def setUp(self, get):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.session = {}
        self.app_name = 'app-test'
        content = u'[{"name": "tsuruteam"}, {"name": "teamvieira"}]'
        m = Mock(status_code=200, content=content)
        m.json.return_value = json.loads(content)
        get.return_value = m
        self.response = AppAddTeam().get(self.request, self.app_name)
        self.request_post = self.factory.post('/', {'team': 'team-test'})
        self.request_post.session = {}
        self.response_mock = Mock()

    def test_should_require_login_to_add_team_to_app(self):
        assert issubclass(AppAddTeam, LoginRequiredView)

    def test_should_render_expected_template(self):
        self.assertIn('apps/app_add_team.html', self.response.template_name)

    def test_context_should_contain_form(self):
        self.assertIn('form', self.response.context_data.keys())

    def test_form_in_context_should_has_a_instance_of_AppAddTeamForm(self):
        form = self.response.context_data.get('form')
        self.assertIsInstance(form, AppAddTeamForm)

    def test_get_request_team_url_should_not_return_404(self):
        response = self.client.get(reverse('app-add-team',
                                   args=[self.app_name]))
        self.assertNotEqual(404, response.status_code)

    @patch('requests.put')
    def test_should_send_request_post_to_tsuru_with_args_expected(self, put):
        self.request_post.session = {'tsuru_token': 'tokentest'}
        AppAddTeam().post(self.request_post, self.app_name)
        self.assertEqual(1, put.call_count)
        put.assert_called_with(
            '%s/apps/app-test/team-test' % settings.TSURU_HOST,
            headers={'authorization':
                     self.request_post.session['tsuru_token']})

    @patch('requests.put')
    def test_post_with_valid_and_team(self, put):
        put.return_value = Mock(status_code=200)
        response = AppAddTeam().post(self.request_post, self.app_name)
        self.assertEqual("The Team was successfully added",
                         response.context_data.get('message'))

    @patch('requests.put')
    def test_post_with_invalid_app_or_team(self, put):
        put.return_value = Mock(content='Error', status_code=500)
        response = AppAddTeam().post(self.request_post, self.app_name)
        self.assertEqual('Error', response.context_data.get('errors'))

    @patch('requests.put')
    def test_post_with_valid_data_should_return_context_with_form(self, put):
        put.return_value = Mock(status_code=200)
        response = AppAddTeam().post(self.request_post, self.app_name)
        self.assertIn('form', response.context_data.keys())
        self.assertIsInstance(response.context_data.get('form'), AppAddTeamForm)

    @patch('requests.put')
    def test_post_with_invalid_data_should_return_context_with_form(self, put):
        put.return_value = Mock(content='Error', status_code=500)
        response = AppAddTeam().post(self.request_post, self.app_name)
        self.assertIn('form', response.context_data.keys())
        self.assertIsInstance(response.context_data.get('form'), AppAddTeamForm)

    @patch('requests.put')
    def test_invalid_post_should_not_send_request_to_tsuru(self, put):
        request = self.factory.post('/', {'team': ''})
        request.session = {}
        AppAddTeam().post(request, self.app_name)
        self.assertEqual(0, put.call_count)

    @patch('requests.put')
    @patch('requests.get')
    def test_post_invalid_form_should_return_form_with_errors(self, get, put):
        content = (u"""[{"name":"teamtsuru"},""" +
                   u"""{"Name":"teamestag"},{"Name":"teambla"}]""")
        m = Mock(status_code=200, content=content)
        m.json.return_value = json.loads(content)
        get.return_value = m
        request = self.factory.post('/', {'team': ''})
        request.session = {}
        response = AppAddTeam().post(request, self.app_name)
        self.assertIn('form', response.context_data.keys())
        form = response.context_data.get('form')
        self.assertIsInstance(form, AppAddTeamForm)
        self.assertEqual(u'This field is required.', form.errors.get('team')[0])
