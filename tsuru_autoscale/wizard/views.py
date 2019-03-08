from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from tsuru_autoscale.wizard import forms
from tsuru_dashboard import settings

from django.template.response import TemplateResponse
from tsuru_autoscale.auth.views import LoginRequiredView

import requests


class Wizard(LoginRequiredView):
    template_name = "wizard/index.html"

    def get(self, request, **kwargs):
        instance = kwargs['instance'] or None

        dlist = [(d["Name"], d["Name"]) for d in self.client.datasource.list().json()]

        scale_up_form = forms.ScaleForm(request.POST or None, prefix="scale_up", initial={"operator": ">"})
        scale_up_form.fields['metric'].choices = dlist

        scale_down_form = forms.ScaleForm(request.POST or None, prefix="scale_down", initial={"operator": "<"})
        scale_down_form.fields['metric'].choices = dlist

        config_form = forms.ConfigForm(request.POST or None)

        p_list = self.process_list(instance)
        config_form.fields['process'].choices = p_list

        if scale_up_form.is_valid() and scale_down_form.is_valid() and config_form.is_valid():
            self.get_or_create_tsuru_instance(instance)
            config_data = {
                "name": instance,
                "minUnits": config_form.cleaned_data["min"],
                "scaleUp": scale_up_form.cleaned_data,
                "scaleDown": scale_down_form.cleaned_data,
                "process": config_form.cleaned_data["process"],
            }
            self.client.wizard.new(config_data)
            messages.success(request, u"Auto scale saved.")
            url = reverse("autoscale-app-info", args=[instance])
            return redirect(url)

        context = {
            "scale_up_form": scale_up_form,
            "scale_down_form": scale_down_form,
            "config_form": config_form,
        }

        return TemplateResponse(request, self.template_name, context)

    def process_list(self, instance):
        response = self.tclient.apps.get(instance)
        app = None
        if response.status_code == 200:
            app = response.json()

        process = set()
        for u in app.get('units', []):
            process.add(u['ProcessName'])

        p_list = []
        for u in list(process):
            p_list.append((u, u))

        return p_list

    def get_or_create_tsuru_instance(self, instance):
        url = "{}/services/autoscale/instances/{}".format(settings.TSURU_HOST, instance)
        headers = self.authorization
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return

        response = self.tclient.apps.get(instance)
        app = None
        if response.status_code == 200:
            app = response.json()

        url = "{}/services/autoscale/instances".format(settings.TSURU_HOST)
        headers += {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"service_name": "autoscale", "name": instance, "owner": app["teamowner"]}
        response = requests.post(url, headers=headers, data=data)

        url = "{}/services/autoscale/instances/{}/{}".format(settings.TSURU_HOST, instance, instance)
        headers = self.authorization
        response = requests.put(url, headers=headers, data={"noRestart": "true"})


class WizardRemove(LoginRequiredView):
    def get(self, request, **kwargs):
        instance = kwargs['instance']
        self.client.wizard.remove(instance)
        messages.success(request, u"Auto scale {} removed.".format(instance), fail_silently=True)
        url = reverse("autoscale-app-info", kwargs={"app": instance})
        return redirect(url)


class WizardEnable(LoginRequiredView):
    def get(self, request, **kwargs):
        instance = kwargs['instance']
        self.client.wizard.enable(instance)
        messages.success(request, u"Auto scale {} enabled.".format(instance), fail_silently=True)
        url = reverse("autoscale-app-info", args=[instance])
        return redirect(url)


class WizardDisable(LoginRequiredView):
    def get(self, request, **kwargs):
        instance = kwargs['instance']
        self.client.wizard.disable(instance)
        messages.success(request, u"Auto scale {} disabled.".format(instance), fail_silently=True)
        url = reverse("autoscale-app-info", args=[instance])
        return redirect(url)
