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
            nodes = sorted(response.json(), key=lambda item: item["ID"])
        return TemplateResponse(request, "docker/list_node.html",
                                {'nodes': nodes})
