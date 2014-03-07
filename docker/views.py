from django.template.response import TemplateResponse
from django.conf import settings

from auth.views import LoginRequiredView

import requests


class ListNode(LoginRequiredView):
    def get(self, request):
        authorization = {'authorization': request.session.get('tsuru_token')}
        response = requests.get('%s/node' % settings.TSURU_HOST,
                                headers=authorization)
        if response.status_code == 204:
            nodes = []
        else:
            nodes = response.json()
            for n in nodes:
                n["Address"] = n["Address"].replace(':4243', '')
        return TemplateResponse(request, "docker/list_node.html",
                                {'nodes': nodes})


class ListContainer(LoginRequiredView):
    def get(self, request, address):
        authorization = {'authorization': request.session.get('tsuru_token')}
        url = '%s/node/%s/containers' % (settings.TSURU_HOST, address)
        response = requests.get(url, headers=authorization)
        if response.status_code == 204:
            containers = []
        containers = response.json()
        return TemplateResponse(request, "docker/list_container.html",
                                {'containers': containers, 'address': address})
