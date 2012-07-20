import json
import requests

from django.views.generic.base import View
from django.template.response import TemplateResponse
from django.conf import settings

from apps.forms import AppForm, AppAddTeamForm, RunForm
from auth.views import LoginRequiredView


class CreateApp(View):

    def get(self, request):
        return TemplateResponse(request, "apps/create.html", {"app_form": AppForm()})

    def post(self, request):
        form = AppForm(request.POST)
        if form.is_valid():
            authorization = {'authorization': request.session.get('tsuru_token')}
            data = form.data
            data.update({"framework": "django"})
            response = requests.post('%s/apps' % settings.TSURU_HOST,
                                     data=json.dumps(form.data),
                                     headers=authorization)
            if response.status_code == 200:
                return TemplateResponse(request, 'apps/create.html', {'form': form, 'message': "App was successfully created"})
            return TemplateResponse(request, 'apps/create.html', {'form': form, 'error': response.content})
        return TemplateResponse(request, 'apps/create.html', {'form': form})


class AppAddTeam(LoginRequiredView):
    template = "apps/app_add_team.html"

    def get(self, request):
        context = {}
        context['form'] = AppAddTeamForm()
        return TemplateResponse(request, self.template, context=context)

    def post(self, request):
        form = AppAddTeamForm(request.POST)
        if not form.is_valid():
            return TemplateResponse(request, self.template, {'form': form})

        authorization = {'authorization': request.session.get('tsuru_token')}
        tsuru_url = '%s/apps/%s/%s' % (settings.TSURU_HOST, form.data.get('app'), form.data.get('team'))
        response = requests.put(tsuru_url, headers=authorization)
        if response.status_code == 200:
            return TemplateResponse(request, self.template, {'form': form, 'message': "The Team was successfully added"})
        return TemplateResponse(request, self.template, {'form': form, 'errors': response.content })

class Run(LoginRequiredView):
    template = "apps/run.html"

    def get(self, request):
        context = {}
        context['form'] = RunForm()
        return TemplateResponse(request, self.template, context=context)

    def post(self, request):
        form = RunForm(request.POST)
        if not form.is_valid():
            return TemplateResponse(request, self.template, {'form': form})

        authorization = {'authorization': request.session.get('tsuru_token')}
        tsuru_url = '%s/apps/%s/run' % (settings.TSURU_HOST, form.data.get('app'))
        response = requests.post(tsuru_url, data=form.data.get('command'), headers=authorization)
        if response.status_code == 200:
            return TemplateResponse(request, self.template, {'form': form, 'message': "The Command was executed with successfully"})
        return TemplateResponse(request, self.template, {'form': form, 'errors': response.content })
