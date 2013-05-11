from django.template.response import TemplateResponse
from django.conf import settings
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from auth.views import LoginRequiredView

import requests


class List(LoginRequiredView):
    def get(self, request):
        auth = {'authorization': request.session.get('tsuru_token')}
        url = "{0}/teams".format(settings.TSURU_HOST)
        teams = requests.get(url, headers=auth).json()
        return TemplateResponse(request, "teams/list.html", {'teams': teams})


class Remove(LoginRequiredView):
    def get(self, request, *args, **kwargs):
        team_name = kwargs["team"]
        auth = {'authorization': request.session.get('tsuru_token')}
        url = "{0}/teams/{1}".format(settings.TSURU_HOST, team_name)
        requests.delete(url, headers=auth)
        return redirect(reverse('team-list'))
