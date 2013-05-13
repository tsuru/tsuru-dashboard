from django.template.response import TemplateResponse
from django.conf import settings
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from auth.views import LoginRequiredView
from teams.forms import TeamForm

import requests
import json


class AddUser(LoginRequiredView):
    def post(self, request, *args, **kwargs):
        team_name = kwargs["team"]
        return redirect(reverse('team-info', args=[team_name]))


class Info(LoginRequiredView):
    def get(self, request, *args, **kwargs):
        context = {"team_name": kwargs["team"]}
        return TemplateResponse(request, "teams/info.html", context)


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


class Add(LoginRequiredView):

    def get(self, request):
        return TemplateResponse(request, 'auth/team.html',
                                {"form": TeamForm()})

    def post(self, request):
        form = TeamForm(request.POST)
        errors = ''
        if form.is_valid():
            authorization = {'authorization':
                             request.session.get('tsuru_token')}
            response = requests.post('{0}/teams'.format(settings.TSURU_HOST),
                                     data=json.dumps(form.data),
                                     headers=authorization)
            if response.status_code == 200:
                return redirect(reverse("team-list"))
            errors = response.content
        return TemplateResponse(request, 'auth/team.html',
                                {'form': form, 'errors': errors})
