import json
import requests

from django.template.response import TemplateResponse
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView

from apps.forms import AppForm, AppAddTeamForm, RunForm, SetEnvForm
from auth.views import LoginRequiredView, LoginRequiredMixin

from pluct import resource


class ChangeUnit(LoginRequiredView):
    def add_unit(self, units, app_name):
        requests.put(
            "{0}/apps/{1}/units".format(settings.TSURU_HOST,
                                        app_name),
            headers=self.authorization,
            data=str(units)
        )

    def remove_units(self, units, app_name):
        requests.delete(
            "{0}/apps/{1}/units".format(settings.TSURU_HOST,
                                        app_name),
            headers=self.authorization,
            data=str(units)
        )

    @property
    def authorization(self):
        return {'authorization': self.request.session.get('tsuru_token')}

    def resource(self, app_name):
        token = self.authorization["authorization"].replace('type ', '')
        auth = {
            'type': 'type',
            'credentials': token,
        }
        url = '{0}/apps/{1}'.format(settings.TSURU_HOST, app_name)
        return resource.get(url, auth)

    def post(self, request, *args, **kwargs):
        app_name = kwargs['app_name']

        app = self.resource(app_name)

        app_units = len(app.data["units"])
        units = int(request.POST["units"])

        if len(app.data["units"]) < int(request.POST['units']):
            self.add_unit(units - app_units, app_name)
        if len(app.data["units"]) > int(request.POST['units']):
            self.remove_units(app_units - units, app_name)
        return redirect(reverse('detail-app', args=[app_name]))


class AppDetail(LoginRequiredMixin, TemplateView):
    template_name = 'apps/details.html'

    @property
    def authorization(self):
        return {'authorization': self.request.session.get('tsuru_token')}

    def service_list(self):
        tsuru_url = '{0}/services'.format(settings.TSURU_HOST)
        return requests.get(tsuru_url, headers=self.authorization).json()

    def service_info(self, instance_name):
        tsuru_url = '{0}/services/instances/{1}'.format(settings.TSURU_HOST,
                                                        instance_name)
        response = requests.get(tsuru_url, headers=self.authorization)
        if response.status_code != 200:
            return {}
        return response.json()

    def get_context_data(self, *args, **kwargs):
        context = super(AppDetail, self).get_context_data(*args, **kwargs)
        app_name = kwargs["app_name"]
        token = self.request.session.get('tsuru_token').replace('type ', '')
        url = '{0}/apps/{1}'.format(settings.TSURU_HOST, app_name)
        headers = {
            'content-type': 'application/json',
            'Authorization': '{} {}'.format('type', token)
        }
        context['app'] = requests.get(url, headers=headers).json()
        service_instances = []
        for service in self.service_list():
            instances = service.get("instances", None)
            instances = instances or []
            for instance in instances:
                instance_data = self.service_info(instance)
                if instance_data != {}:
                    app_name = context['app']['name']
                    if app_name in instance_data['Apps']:
                        service_instances.append(
                            {"name": instance_data["Name"],
                             "servicename": instance_data["ServiceName"]}
                        )
        context['app']["service_instances"] = service_instances
        return context


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
        return redirect(reverse('list-app'))


class CreateApp(LoginRequiredView):
    def get(self, request):
        context = {
            "app_form": AppForm(),
            "platforms": self._get_platforms(request),
        }
        return TemplateResponse(request, "apps/create.html", context)

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
                context['message'] = "App was successfully created"
            else:
                context['errors'] = response.content
                context['platforms'] = self._get_platforms(request)
        else:
            context['platforms'] = self._get_platforms(request)
        context['app_form'] = form
        return TemplateResponse(request, 'apps/create.html', context)

    def _get_platforms(self, request):
        authorization = {"authorization": request.session.get("tsuru_token")}
        response = requests.get("%s/platforms" % settings.TSURU_HOST,
                                headers=authorization)
        platforms = response.json()
        return [p["Name"] for p in platforms]


class ListApp(LoginRequiredView):
    def get(self, request):
        authorization = {'authorization': request.session.get('tsuru_token')}
        response = requests.get('%s/apps' % settings.TSURU_HOST,
                                headers=authorization)
        if response.status_code == 204:
            apps = []
        else:
            apps = sorted(response.json(), key=lambda item: item["name"])
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
                                {'logs': response, 'app': app})


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
