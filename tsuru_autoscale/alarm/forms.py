from django import forms


def datasource_list(token):
    from tsuru_autoscale.datasource import client
    dl = client.list(token).json() or []
    return [(ds['Name'], ds['Name']) for ds in dl]


def action_list(token):
    from tsuru_autoscale.action import client
    al = client.list(token).json() or []
    return [(ds['Name'], ds['Name']) for ds in al]


def service_instance_list(token):
    from tsuru_autoscale.alarm import client
    al = client.service_instance_list(token).json() or []
    return [(ds['Name'], ds['Name']) for ds in al]


class AlarmForm(forms.Form):
    name = forms.CharField()
    expression = forms.CharField()
    enabled = forms.BooleanField(initial=True)
    wait = forms.IntegerField()
    datasource = forms.ChoiceField()
    actions = forms.MultipleChoiceField()
    instance = forms.ChoiceField()
