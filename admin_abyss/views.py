from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.response import TemplateResponse
from django.conf import settings

from auth.views import LoginRequiredView

import requests
import json
import re


class ListNode(LoginRequiredView):
    def get(self, request):
        authorization = {'authorization': request.session.get('tsuru_token')}
        response = requests.get('%s/docker/node' % settings.TSURU_HOST,
                                headers=authorization)
        if response.status_code == 204:
            nodes = []
        else:
            nodes = sorted(response.json(), key=lambda item: item["ID"])
            for n in nodes:
                n["Address"] = n["Address"].replace(':4243', '')
        return TemplateResponse(request, "docker/list_node.html",
                                {'nodes': nodes})


class ListContainer(LoginRequiredView):
    def get(self, request, address):
        authorization = {'authorization': request.session.get('tsuru_token')}
        url = '%s/docker/node/%s/containers' % (settings.TSURU_HOST, address)
        response = requests.get(url, headers=authorization)
        if response.status_code == 204:
            containers = []
        containers = response.json()
        return TemplateResponse(request, "docker/list_container.html",
                                {'containers': containers, 'address': address})


class ListContainersByApp(LoginRequiredView):
    def get(self, request, appname):
        authorization = {'authorization': request.session.get('tsuru_token')}
        url = "{0}/docker/node/apps/{1}/containers".format(settings.TSURU_HOST,
                                                           appname)
        response = requests.get(url, headers=authorization)
        if response.status_code == 204:
            containers = []
        containers = response.json()
        return TemplateResponse(request, "apps/list_containers.html",
                                {'containers': containers, 'appname': appname})


class ListDeploy(LoginRequiredView):
    template = "deploys/list_deploys.html"

    def get(self, request):
        context = {}
        context['services'] = self._get_services(request)
        qr_string = request.GET.get('service', '')
        authorization = {'authorization': request.session.get('tsuru_token')}
        response = requests.get('%s/deploys?service=%s' % (settings.TSURU_HOST,
                                qr_string), headers=authorization)
        if response.status_code == 204:
            deploys = []
        else:
            deploys = response.json()

        paginator = Paginator(deploys, 20)
        page = request.GET.get('page')
        try:
            deploys = paginator.page(page)
        except PageNotAnInteger:
            deploys = paginator.page(1)
        except EmptyPage:
            deploys = paginator.page(paginator.num_pages)

        context['deploys'] = deploys
        context['paginator'] = paginator
        context['is_paginated'] = True
        context['current'] = qr_string
        return TemplateResponse(request, self.template, context=context)

    def _get_services(self, request):
        authorization = {"authorization": request.session.get("tsuru_token")}
        response = requests.get("%s/services/instances" % settings.TSURU_HOST,
                                headers=authorization)
        services = response.json()
        return [s["service"] for s in services]


class DeploysGraph(LoginRequiredView):
    template = "deploys/deploys_graph.html"

    def get(self, request):
        context = {}
        authorization = {'authorization': request.session.get('tsuru_token')}
        response = requests.get('%s/deploys' % (settings.TSURU_HOST),
                                headers=authorization)
        if response.status_code == 204:
            deploys = []
        else:
            deploys = response.json()

        appFilter = request.GET.get('app', None)
        appExclude = request.GET.get('appExclude', None)
        minTime = request.GET.get('minTime', None)
        maxTime = request.GET.get('maxTime', None)

        deploysByApp = {}
        for deploy in reversed(deploys):
            if deploy["Duration"] == 0:
                continue

            minutes = deploy["Duration"] / (1000 * 1000 * 1000.0 * 60)
            appName = deploy["App"]

            if appFilter and not re.search(appFilter, appName):
                continue
            if appExclude and re.search(appExclude, appName):
                continue
            if minTime and minutes < int(minTime):
                continue
            if maxTime and minutes > int(maxTime):
                continue

            appEntry = deploysByApp.get(appName)
            if appEntry is None:
                appEntry = {}
                appEntry["key"] = appName
                deploysByApp[appName] = appEntry
            values = appEntry.get("values", [])
            values.append({
                "x": deploy["Timestamp"],
                "y": minutes,
            })
            appEntry["values"] = values

        context['deploys'] = json.dumps([app for app in deploysByApp.values()])
        return TemplateResponse(request, self.template, context=context)


class ListAppAdmin(LoginRequiredView):
    def get(self, request):
        authorization = {'authorization': request.session.get('tsuru_token')}
        response = requests.get('%s/apps' % settings.TSURU_HOST,
                                headers=authorization)
        if response.status_code == 204:
            apps = []
        else:
            apps = sorted(response.json(), key=lambda item: item["name"])
        return TemplateResponse(request, "apps/list_app_admin.html",
                                         {'apps': apps})
