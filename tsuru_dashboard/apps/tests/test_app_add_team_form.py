from django.test import TestCase
from django.forms import CharField

from tsuru_dashboard.apps import forms


class AppAddTeamFormTest(TestCase):
    def test_forms_should_contains_AppAddTeamForm(self):
        self.assertTrue(hasattr(forms, 'AppAddTeamForm'))

    def test_should_have_team_field(self):
        self.assertIn('team', forms.AppAddTeamForm.base_fields)

    def test_team_field_should_have_CharField(self):
        field = forms.AppAddTeamForm.base_fields['team']
        self.assertIsInstance(field, CharField)

    def test_team_field_should_have_at_most_60_characters(self):
        field = forms.AppAddTeamForm.base_fields['team']
        self.assertEqual(60, field.max_length)
