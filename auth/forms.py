from django import forms
from django.forms import widgets

class LoginForm(forms.Form):
	username = forms.EmailField(max_length=60)
	password = forms.CharField(widget=widgets.PasswordInput, min_length=6)

class TeamForm(forms.Form):
    pass

class SignupForm(forms.Form):
    email = forms.EmailField(max_length=60)
    password = forms.CharField(widget=widgets.PasswordInput, min_length=6)
    same_password_again = forms.CharField(widget=widgets.PasswordInput, min_length=6)