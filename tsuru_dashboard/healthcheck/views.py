from django.http import HttpResponse

from tsuru_dashboard import settings

import requests


def healthcheck(request):
    url = "{0}/healthcheck/".format(settings.TSURU_HOST)

    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        return HttpResponse("Failed to connect to tsuru.", status=500)

    if response.status_code != 200 or response.text != "WORKING":
        return HttpResponse("Failed to connect to tsuru.", status=500)

    return HttpResponse("WORKING", status=200)
