from django.shortcuts import render

from tsuru_autoscale.event import client


def list(request, alarm_name):
    token = request.session.get("TSURU_TOKEN")
    events = client.list(alarm_name, token).json()
    context = {
        "list": events,
    }
    return render(request, "event/list.html", context)
