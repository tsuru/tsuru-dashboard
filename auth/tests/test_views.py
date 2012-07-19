from django.test import TestCase
from django.test.client import RequestFactory
from django.http import Http404

from auth.views import login, team
from auth.forms import TeamForm


class LoginViewTest(TestCase):
    def test_login_expected_template_view(self):
        request = RequestFactory().get('/')
        response = login(request)
        self.assertEqual('auth/login.html', response.template_name)


class TeamViewTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/')
        self.response = team(self.request)

    def test_team_should_render_expected_template(self):
        self.assertEqual('auth/team.html', self.response.template_name)

    def test_context_should_contain_form(self):
        self.assertIn('form', self.response.context_data.keys())

    def test_form_in_context_should_has_a_instance_of_TeamForm(self):
        form = self.response.context_data.get('form')
        self.assertTrue(isinstance(form, TeamForm))

    def test_get_request_team_url_should_return_200(self):
        try:
            self.client.get('/team/')
        except Http404:
            assert False
