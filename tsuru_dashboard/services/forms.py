from django import forms


class ServiceForm(forms.Form):
    name = forms.CharField(max_length=50)
