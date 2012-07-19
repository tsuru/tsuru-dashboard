from django import forms


class AppForm(forms.Form):
    name = forms.CharField(max_length=60)
