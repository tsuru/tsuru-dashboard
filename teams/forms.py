from django import forms


class TeamForm(forms.Form):
    name = forms.CharField(max_length=60)
