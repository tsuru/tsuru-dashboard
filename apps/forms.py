from django import forms


class AppForm(forms.Form):
    name = forms.CharField(max_length=60)
    platform = forms.ChoiceField()
    plan = forms.ChoiceField(required=False)
    teamOwner = forms.ChoiceField(required=False)
    pool = forms.ChoiceField(required=False)


class AppAddTeamForm(forms.Form):
    team = forms.CharField(max_length=60)


class RunForm(forms.Form):
    app = forms.CharField(max_length=60)
    command = forms.CharField(max_length=1000)


class SetEnvForm(forms.Form):
    env = forms.CharField(max_length=1000)
