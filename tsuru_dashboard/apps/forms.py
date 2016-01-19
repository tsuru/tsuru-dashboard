from django import forms


class AppForm(forms.Form):
    name = forms.CharField(max_length=60)
    platform = forms.ChoiceField()
    plan = forms.ChoiceField(required=False)
    teamOwner = forms.ChoiceField(required=False)
    pool = forms.ChoiceField(required=False)
