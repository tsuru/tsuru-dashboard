from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.contrib import messages

from tsuru_dashboard import settings
from tsuru_dashboard.auth.views import LoginRequiredView

import requests


class ListService(LoginRequiredView, TemplateView):
    template_name = "services/list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ListService, self).get_context_data(*args, **kwargs)
        url = "{}/services/instances".format(settings.TSURU_HOST)
        services = []
        resp = requests.get(url, headers=self.authorization)
        if resp.status_code == 200:
            services = resp.json()
        context.update({"services": services})
        return context


class ServiceInstanceDetail(LoginRequiredView, TemplateView):
    template_name = "services/detail.html"

    def apps(self, instance):
        url = "{}/apps".format(settings.TSURU_HOST)
        response = requests.get(url, headers=self.authorization)
        app_list = []
        for app in response.json():
            if app['name'] not in instance['Apps']:
                app_list.append(app['name'])
        return app_list

    def get_instance(self, service_name, instance_name):
        url = "{}/services/{}/instances/{}".format(settings.TSURU_HOST, service_name, instance_name)
        response = requests.get(url, headers=self.authorization)
        return response.json()

    def get_context_data(self, *args, **kwargs):
        context = super(ServiceInstanceDetail, self).get_context_data(*args, **kwargs)
        instance_name = kwargs["instance"]
        service_name = kwargs["service"]
        instance = self.get_instance(service_name, instance_name)
        apps = self.apps(instance)
        context.update(
            {
                "instance": instance,
                "apps": apps,
                "service_name": service_name,
                "instance_name": instance_name
            }
        )

        return context


class ServiceAdd(LoginRequiredView):
    def post(self, request, *args, **kwargs):
        service_name = kwargs["service_name"]
        url = '{}/services/{}/instances'.format(settings.TSURU_HOST, service_name)
        data = {
            "name": request.POST["name"],
            "owner": request.POST["team"],
        }
        response = requests.post(url, data=data, headers=self.authorization)

        if response.status_code == 201:
            messages.success(request, u'Instance was successfully created', fail_silently=True)
            return redirect(reverse('service-list'))

        messages.error(request, response.content, fail_silently=True)
        return redirect(reverse('service-add', args=[service_name]))

    def get(self, request, *args, **kwargs):
        service_name = kwargs["service_name"]
        url = "{}/teams".format(settings.TSURU_HOST)
        response = requests.get(url, headers=self.authorization)
        teams = response.json()
        context = {
            "service": {"name": service_name},
            "teams": teams,
        }
        return TemplateResponse(request, "services/add.html", context)


class Bind(LoginRequiredView):
    def post(self, request, *args, **kwargs):
        app = request.POST["app"]
        instance = kwargs["instance"]
        service = kwargs["service"]

        url = '{}/services/{}/instances/{}/{}'.format(settings.TSURU_HOST, service, instance, app)
        requests.put(url, headers=self.authorization)

        return redirect(reverse('service-detail', args=[service, instance]))


class Unbind(LoginRequiredView):
    def get(self, request, *args, **kwargs):
        app = kwargs["app"]
        instance = kwargs["instance"]
        service = kwargs["service"]

        url = '{}/services/{}/instances/{}/{}'.format(settings.TSURU_HOST, service, instance, app)
        requests.delete(url, headers=self.authorization)

        return redirect(reverse('service-detail', args=[service, instance]))


class ServiceRemove(LoginRequiredView):
    def get(self, request, *args, **kwargs):
        instance = kwargs["instance"]
        service = kwargs["service"]

        url = '{}/services/{}/instances/{}'.format(settings.TSURU_HOST, service, instance)
        requests.delete(url, headers=self.authorization)

        return redirect(reverse('service-list'))
