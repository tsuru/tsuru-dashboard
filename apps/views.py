import json
import requests

from django.template.response import TemplateResponse
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from apps.forms import AppForm, AppAddTeamForm, RunForm, SetEnvForm
from auth.views import LoginRequiredView

from pluct import resource


class UnitAdd(LoginRequiredView):
    def post(self, request, *args, **kwargs):
        app_name = kwargs['app_name']
        authorization = {'authorization': request.session.get('tsuru_token')}
        requests.put(
            "{0}/apps/app_name/units".format(settings.TSURU_HOST, app_name),
            headers=authorization,
            data=request.POST['units']
        )
        return HttpResponse('', status=200)


class UnitRemove(LoginRequiredView):
    def post(self, request, *args, **kwargs):
        app_name = kwargs['app_name']
        authorization = {'authorization': request.session.get('tsuru_token')}
        requests.delete(
            "{0}/apps/app_name/units".format(settings.TSURU_HOST, app_name),
            headers=authorization,
            data=request.POST['units']
        )
        return HttpResponse('', status=200)


class AppDetail(LoginRequiredView):
    def get(self, request, *args, **kwargs):
        app_name = kwargs["app_name"]
        token = request.session.get('tsuru_token').replace('type ', '')
        auth = {
            'type': 'type',
            'credentials': token,
        }
        url = '{0}/apps/{1}'.format(settings.TSURU_HOST, app_name)
        app = resource.get(url, auth)
        return TemplateResponse(request, "apps/details.html",
                                {"app": app.data})


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
        return HttpResponseRedirect(reverse('list-app'))


class CreateApp(LoginRequiredView):
    def get(self, request):
        return TemplateResponse(request, "apps/create.html",
                                {"app_form": AppForm()})

    def post(self, request):
        context = {}
        form = AppForm(request.POST)
        if form.is_valid():
            authorization = {'authorization':
                             request.session.get('tsuru_token')}
            response = requests.post(
                '%s/apps' % settings.TSURU_HOST,
                data=json.dumps(form.data),
                headers=authorization
            )
            if response.status_code == 200:
                context.update({'message': "App was successfully created"})
            else:
                context.update({'errors': response.content})
        context.update({'app_form': form})
        return TemplateResponse(request, 'apps/create.html', context)


class ListApp(LoginRequiredView):
    def get(self, request):
        authorization = {'authorization': request.session.get('tsuru_token')}
        response = requests.get('%s/apps' % settings.TSURU_HOST,
                                headers=authorization)
        apps = response.json
        return TemplateResponse(request, "apps/list.html", {'apps': apps})


class AppAddTeam(LoginRequiredView):
    template = "apps/app_add_team.html"

    def get(self, request, app_name):
        context = {}
        context['app_name'] = app_name
        context['form'] = AppAddTeamForm()
        return TemplateResponse(request, self.template, context=context)

    def post(self, request, app_name):
        form = AppAddTeamForm(request.POST)
        if not form.is_valid():
            return TemplateResponse(request, self.template, {'form': form})

        authorization = {'authorization': request.session.get('tsuru_token')}
        tsuru_url = '%s/apps/%s/%s' % (settings.TSURU_HOST, app_name,
                                       form.data.get('team'))
        response = requests.put(tsuru_url, headers=authorization)
        if response.status_code == 200:
            return TemplateResponse(
                request, self.template,
                {'form': form, 'app_name': app_name,
                 'message': "The Team was successfully added"}
            )
        return TemplateResponse(request, self.template,
                                {'form': form, 'app_name': app_name,
                                 'errors': response.content})


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
        tsuru_url = '%s/apps/%s/run' % (settings.TSURU_HOST,
                                        form.data.get('app'))
        response = requests.post(tsuru_url, data=form.data.get('command'),
                                 headers=authorization)
        if response.status_code == 200:
            return TemplateResponse(request, self.template,
                                    {'form': form,
                                     'message': response.content})
        return TemplateResponse(request, self.template,
                                {'form': form, 'errors': response.content})


class AppLog(LoginRequiredView):
    template = "apps/app_log.html"

    def get(self, request, app_name):
        token = request.session.get('tsuru_token').replace('type ', '')
        auth = {
            'type': 'type',
            'credentials': token,
        }
        url = '{0}/apps/{1}'.format(settings.TSURU_HOST, app_name)
        app = resource.get(url, auth)
        response = app.log(lines=10)
        return TemplateResponse(request, self.template,
                                {'logs': response.json(), 'app': app_name})


class AppTeams(LoginRequiredView):
    template = "apps/app_team.html"

    def get(self, request, app_name):
        authorization = {'authorization': request.session.get('tsuru_token')}
        tsuru_url = '%s/apps/%s' % (settings.TSURU_HOST, app_name)
        response = requests.get(tsuru_url, headers=authorization)

        if response.status_code == 200:
            app = response.json
            return TemplateResponse(request, self.template, {'app': app})
        return TemplateResponse(request, self.template,
                                {'errors': response.content})


class AppEnv(LoginRequiredView):
    template = "apps/app_env.html"

    def get(self, request, app_name):
        context = {}
        context['app'] = app_name
        context['form'] = SetEnvForm(initial=context)

        response = self.get_envs(request, app_name)

        if response.status_code == 200:
            envs = response.content.split('\n')
            context['envs'] = envs
            return TemplateResponse(request, self.template, context)
        return TemplateResponse(request, self.template,
                                {'errors': response.content})

    def post(self, request, app_name):
        context = {}
        context['app'] = app_name

        response = self.get_envs(request, app_name)
        if response.status_code == 200:
            form = SetEnvForm(request.POST)
            context['form'] = form
            if not form.is_valid():
                return TemplateResponse(request, self.template, context)

            envs = response.content.split('\n')
            envs.append(request.POST['env'])
            context['envs'] = envs

            response = self.set_env(request, app_name, form)

            if response.status_code == 200:
                context['message'] = response.content
                return TemplateResponse(request, self.template, context)

        context['errors'] = response.content
        return TemplateResponse(request, self.template, context)

    def get_envs(self, request, app_name):
        authorization = {'authorization': request.session.get('tsuru_token')}
        tsuru_url = '%s/apps/%s/env' % (settings.TSURU_HOST, app_name)
        return requests.get(tsuru_url, headers=authorization)

    def set_env(self, request, app_name, form):
        authorization = {'authorization': request.session.get('tsuru_token')}
        tsuru_url = '%s/apps/%s/env' % (settings.TSURU_HOST, app_name)
        return requests.post(tsuru_url, data=form.data.get('env'),
                             headers=authorization)
