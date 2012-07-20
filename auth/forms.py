from django import forms
from django.forms import widgets


class LoginForm(forms.Form):
	username = forms.EmailField(max_length=60)
	password = forms.CharField(widget=widgets.PasswordInput, min_length=6)


class TeamForm(forms.Form):
    name = forms.CharField(max_length=60)


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
    same_password_again = forms.CharField(widget=widgets.PasswordInput, min_length=6)

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
    key = forms.CharField(max_length=2000)
