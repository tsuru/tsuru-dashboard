from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from tsuru_autoscale.alarm.forms import AlarmForm, datasource_list, action_list, service_instance_list
from tsuru_autoscale.alarm import client


def new(request):
    token = request.session.get("TSURU_TOKEN")

    form = AlarmForm(request.POST or None)
    form.fields['datasource'].choices = datasource_list(token)
    form.fields['actions'].choices = action_list(token)
    form.fields['instance'].choices = service_instance_list(token)

    if form.is_valid():
        client.new(form.cleaned_data, token)
        messages.success(request, u"Alarm saved.")
        url = reverse("alarm-list")
        return redirect(url)

    context = {"form": form}
    return render(request, "alarm/new.html", context)


def list(request):
    token = request.session.get("TSURU_TOKEN")
    alarms = client.list(token).json()
    context = {
        "list": alarms,
    }
    return render(request, "alarm/list.html", context)


def remove(request, name):
    token = request.session.get("TSURU_TOKEN")
    client.remove(name, token)
    messages.success(request, u"Alarm {} removed.".format(name))
    url = reverse('alarm-list')
    return redirect(url)


def get(request, name):
    token = request.session.get("TSURU_TOKEN")
    alarm = client.get(name, token).json()
    context = {
        "item": alarm,
    }
    return render(request, "alarm/get.html", context)
