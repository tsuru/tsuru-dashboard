import re

from django import forms
from django.core import validators

team_name = re.compile(r"^[a-zA-Z][-@_.+\w\s]+$")
invalid_team_msg = ("Team name must start with a letter and "
                    "have at least two characters.")
team_name_validator = validators.RegexValidator(regex=team_name,
                                                message=invalid_team_msg)


class TeamForm(forms.Form):
    name = forms.CharField(max_length=60, validators=[team_name_validator])
