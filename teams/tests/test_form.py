from django.utils.unittest import TestCase
from django.forms import CharField

from teams import forms


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
