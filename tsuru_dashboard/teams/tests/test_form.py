from django.test import TestCase
from django.forms import CharField

from tsuru_dashboard.teams import forms


class TeamFormTest(TestCase):
    def test_forms_should_have_TeamForm(self):
        self.assertTrue(hasattr(forms, 'TeamForm'))

    def test_team_should_have_name_field(self):
        self.assertIn('name', forms.TeamForm.base_fields)

    def test_name_field_should_instance_of_CharField(self):
        field = forms.TeamForm.base_fields['name']
        self.assertIsInstance(field, CharField)

    def test_name_should_have_at_most_60_characters(self):
        field = forms.TeamForm.base_fields['name']
        self.assertEqual(60, field.max_length)

    def test_validate_name(self):
        invalid_names = [" ", "", "1 my team", "a"]
        valid_names = ["ab", "cd", "team123", "me@myteam.com",
                       "team-1", "team_2", "me+tsuru@me.com"]
        for name in invalid_names:
            form = forms.TeamForm({"name": name})
            self.assertFalse(form.is_valid(),
                             "{} should be invalid".format(name))
        for name in valid_names:
            form = forms.TeamForm({"name": name})
            self.assertTrue(form.is_valid(),
                            "{} should be valid".format(name))
