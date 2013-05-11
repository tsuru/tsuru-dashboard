from django.template.response import TemplateResponse
from django.conf import settings

from auth.views import LoginRequiredView

import requests


class List(LoginRequiredView):
    def get(self, request):
        auth = {'authorization': request.session.get('tsuru_token')}
        url = "{0}/teams".format(settings.TSURU_HOST)
        teams = requests.get(url, headers=auth).json()
        return TemplateResponse(request, "teams/list.html", {'teams': teams})
