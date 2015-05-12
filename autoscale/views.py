from django.shortcuts import render

import os


def index(request):
    context = {
        "service_url": os.environ.get("AUTOSCALE_DASHBOARD_URL"),
    }
    return render(request, "autoscale/index.html", context)
