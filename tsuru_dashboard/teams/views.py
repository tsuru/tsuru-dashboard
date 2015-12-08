from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import TemplateView
from django.template.response import TemplateResponse

from tsuru_dashboard import settings
from tsuru_dashboard.auth.views import LoginRequiredView

from .forms import TeamForm

import requests
import json


class RemoveUser(LoginRequiredView):
    def get(self, request, *args, **kwargs):
        team_name = kwargs["team"]
        user = kwargs["user"]
        url = "{}/teams/{}/{}".format(settings.TSURU_HOST, team_name, user)
        response = requests.delete(url, headers=self.authorization)

        if response.status_code < 399:
            messages.success(self.request, u'User successfully removed!', fail_silently=True)
        else:
            messages.error(self.request, response.text, fail_silently=True)

        return redirect(reverse('team-info', args=[team_name]))


class AddUser(LoginRequiredView):
    def post(self, request, *args, **kwargs):
        team_name = kwargs["team"]
        user = request.POST["user"]
        url = "{0}/teams/{1}/{2}".format(settings.TSURU_HOST, team_name, user)
        response = requests.put(url, headers=self.authorization)
        if response.status_code != 200:
            messages.error(self.request, response.text, fail_silently=True)
        return redirect(reverse('team-info', args=[team_name]))


class Info(LoginRequiredView, TemplateView):
    template_name = "teams/info.html"

    def get_context_data(self, *args, **kwargs):
        context = super(Info, self).get_context_data(*args, **kwargs)
        url = "{0}/teams/{1}".format(settings.TSURU_HOST, kwargs["team"])
        response = requests.get(url, headers=self.authorization)
        context.update({"team": response.json()})
        return context


class List(LoginRequiredView, TemplateView):
    template_name = "teams/list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(List, self).get_context_data(*args, **kwargs)

        url = "{}/teams".format(settings.TSURU_HOST)
        response = requests.get(url, headers=self.authorization)

        teams = []
        if response.status_code != 204:
            teams = response.json()

        context.update({"teams": teams})
        return context


class Remove(LoginRequiredView):
    def get(self, request, *args, **kwargs):
        team_name = kwargs["team"]
        auth = {'authorization': request.session.get('tsuru_token')}
        url = "{0}/teams/{1}".format(settings.TSURU_HOST, team_name)
        response = requests.delete(url, headers=auth)

        if response.status_code > 399:
            messages.error(self.request, u'Can not delete this team!', fail_silently=True)
        return redirect(reverse('team-list'))


class Add(LoginRequiredView):
    def get(self, request):
        return TemplateResponse(request, 'auth/team.html', {"form": TeamForm()})

    def post(self, request):
        form = TeamForm(request.POST)
        errors = ''
        if form.is_valid():
            url = '{}/teams'.format(settings.TSURU_HOST)
            response = requests.post(url, data=json.dumps(form.data), headers=self.authorization)
            if response.status_code == 200:
                return redirect(reverse("team-list"))
            errors = response.content
        return TemplateResponse(request, 'auth/team.html', {'form': form, 'errors': errors})
