from django import forms
from django.forms import widgets
from tsuru_dashboard import settings

import requests


class ChangePasswordForm(forms.Form):
    old = forms.CharField(widget=forms.PasswordInput())
    new = forms.CharField(widget=forms.PasswordInput())
    confirm = forms.CharField(widget=forms.PasswordInput())


class PasswordRecoveryForm(forms.Form):
    email = forms.EmailField()
    token = forms.CharField()

    def send(self):
        url = "{0}/users/{1}/password?token={2}".format(
            settings.TSURU_HOST,
            self.cleaned_data['email'],
            self.cleaned_data['token']
        )
        requests.post(url)


class TokenRequestForm(forms.Form):
    email = forms.EmailField()

    def send(self):
        url = "{0}/users/{1}/password".format(settings.TSURU_HOST,
                                              self.cleaned_data['email'])
        requests.post(url)


class LoginForm(forms.Form):
    username = forms.EmailField(max_length=60, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=widgets.PasswordInput(attrs={'placeholder': 'Password'}), min_length=6)


class AddUserToTeamForm(forms.Form):

    def __init__(self, teams=None, *args, **kwargs):
        super(AddUserToTeamForm, self).__init__(*args, **kwargs)
        if teams:
            choices = []
            for team in teams:
                choices.append((team, team))
                self.fields["team"].choices = choices

    email = forms.EmailField(max_length=60)
    team = forms.ChoiceField(choices=[])


class SignupForm(forms.Form):
    email = forms.EmailField(max_length=60)
    password = forms.CharField(widget=widgets.PasswordInput, min_length=6)
    same_password_again = forms.CharField(widget=widgets.PasswordInput,
                                          min_length=6)

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        password = cleaned_data.get("password")
        same_password_again = cleaned_data.get("same_password_again")

        if not password == same_password_again:
            msg = "You must type the same password twice!"
            self._errors["same_password_again"] = self.error_class([msg])
            raise forms.ValidationError(msg)

        return cleaned_data


class KeyForm(forms.Form):
    name = forms.CharField()
    key = forms.CharField(widget=forms.Textarea)
