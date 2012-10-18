import json
import requests

from django.template.response import TemplateResponse
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect

from apps.forms import AppForm, AppAddTeamForm, RunForm, SetEnvForm
from auth.views import LoginRequiredView


class AppDetail(LoginRequiredView):
    def get(self, request, *args, **kwargs):
        app_name = kwargs["app_name"]
        authorization = {'authorization': request.session.get('tsuru_token')}
        response = requests.get('{0}/apps/{1}'.format(settings.TSURU_HOST, app_name), headers=authorization)
        app = response.json
        return TemplateResponse(request, "apps/details.html", {"app": app})


class RemoveApp(LoginRequiredView):
    def get(self, request, *args, **kwargs):
        app_name = self.kwargs["name"]
        authorization = {'authorization': request.session.get('tsuru_token')}
        response = requests.delete(
            "{0}/apps/{1}".format(settings.TSURU_HOST, app_name),
            headers=authorization
        )
        if response.status_code > 399:
            return HttpResponse(response.text, status=response.status_code)
        return HttpResponseRedirect("/app")


class CreateApp(LoginRequiredView):
    def get(self, request):
        return TemplateResponse(request, "apps/create.html", {"app_form": AppForm()})

    def post(self, request):
        form = AppForm(request.POST)
        if form.is_valid():
            authorization = {'authorization': request.session.get('tsuru_token')}
            response = requests.post('%s/apps' % settings.TSURU_HOST,
                                     data=json.dumps(form.data),
                                     headers=authorization)
            if response.status_code == 200:
                return TemplateResponse(request, 'apps/create.html', {'form': form, 'message': "App was successfully created"})
            return TemplateResponse(request, 'apps/create.html', {'form': form, 'error': response.content})
        return TemplateResponse(request, 'apps/create.html', {'form': form})


class ListApp(LoginRequiredView):
    def get(self, request):
        authorization = {'authorization': request.session.get('tsuru_token')}
        response = requests.get('%s/apps' % settings.TSURU_HOST, headers=authorization)
        apps = response.json
        return TemplateResponse(request, "apps/list.html", {'apps':apps})


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
            return TemplateResponse(request, self.template, {'form': form, 'message': response.content})
        return TemplateResponse(request, self.template, {'form': form, 'errors': response.content })


class SetEnv(LoginRequiredView):
    template = "apps/set_env.html"

    def get(self, request):
        context = {}
        context['form'] = SetEnvForm()
        return TemplateResponse(request, self.template, context)

    def post(self, request):
        form = SetEnvForm(request.POST)
        if not form.is_valid():
            return TemplateResponse(request, self.template, {'form': form})

        authorization = {'authorization': request.session.get('tsuru_token')}
        tsuru_url = '%s/apps/%s/env' % (settings.TSURU_HOST, form.data.get('app'))
        response = requests.post(tsuru_url, data=form.data.get('env'), headers=authorization)

        if response.status_code == 200:
            return TemplateResponse(request, self.template, {'form': form, 'message': response.content})
        return TemplateResponse(request, self.template, {'form': form, 'errors': response.content })


class AppLog(LoginRequiredView):
    template = "apps/app_log.html"

    def get(self, request, app_name):
        authorization = {'authorization': request.session.get('tsuru_token')}
        tsuru_url = '%s/apps/%s/log' % (settings.TSURU_HOST, app_name)
        response = requests.get(tsuru_url, headers=authorization)

        if response.status_code == 200:
            return TemplateResponse(request, self.template, {'log': response.content, 'app': app_name})
        return TemplateResponse(request, self.template, {'errors': response.content})
