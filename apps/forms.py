from django import forms


class AppForm(forms.Form):
    name = forms.CharField(max_length=60)


class AppAddTeamForm(forms.Form):
    app = forms.CharField(max_length=60)
    team = forms.CharField(max_length=60)
