from django import forms


class AppForm(forms.Form):
    name = forms.CharField(max_length=60)
    framework = forms.CharField(max_length=60)


class AppAddTeamForm(forms.Form):
    app = forms.CharField(max_length=60)
    team = forms.CharField(max_length=60)

class RunForm(forms.Form):
    app = forms.CharField(max_length=60)
    command = forms.CharField(max_length=1000)

class SetEnvForm(forms.Form):
    app = forms.CharField(max_length=60)
    env = forms.CharField(max_length=1000)
