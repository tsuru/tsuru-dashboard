from django.utils.unittest import TestCase
from django.forms import CharField

from apps import forms


class AppRevokeTeamFormTest(TestCase):
    def test_forms_should_contains_AppRevokreTeamForm(self):
        self.assertTrue(hasattr(forms, 'AppRevokeTeamForm'))

    def test_should_have_team_field(self):
        self.assertIn('team', forms.AppRevokeTeamForm.base_fields)

    def test_team_field_should_have_CharField(self):
        field = forms.AppRevokeTeamForm.base_fields['team']
        self.assertTrue(isinstance(field, CharField))

    def test_team_field_should_have_at_most_60_characters(self):
        field = forms.AppRevokeTeamForm.base_fields['team']
        self.assertEqual(60, field.max_length)
