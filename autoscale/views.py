from django.shortcuts import render

import os


def index(request):
    token = request.session.get('tsuru_token').split(' ')[1]

    context = {
        "service_url": "{}?TSURU_TOKEN={}".format(os.environ.get("AUTOSCALE_DASHBOARD_URL"), token),
    }

    return render(request, "autoscale/index.html", context)
