from django.forms import EmailField
from django.test import TestCase

from tsuru_dashboard.auth import forms


class AddUserToTeamFormTest(TestCase):

    def test_should_have_email_and_team_fields(self):
        self.assertIn('email', forms.AddUserToTeamForm.base_fields)
        self.assertIn('team', forms.AddUserToTeamForm.base_fields)

    def test_email_should_have_at_most_60_characters(self):
        field = forms.AddUserToTeamForm.base_fields['email']
        self.assertEqual(60, field.max_length)

    def test_email_field_should_accept_only_email_values(self):
        field = forms.AddUserToTeamForm.base_fields['email']
        self.assertIsInstance(field, EmailField)

    def test_should_receive_list_of_choices_via_constructor(self):
        form = forms.AddUserToTeamForm(teams=["team1", "team2"])
        expected = [("team1", "team1"), ("team2", "team2")]
        self.assertEqual(expected, form.fields["team"].choices)
        self.assertEqual(expected, form.fields["team"].widget.choices)

    def test_choices_should_be_empty_when_no_team_list_is_given(self):
        form = forms.AddUserToTeamForm()
        self.assertEqual([], form.fields["team"].choices)
