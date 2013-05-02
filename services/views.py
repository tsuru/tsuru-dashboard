from django.template.response import TemplateResponse
from django.conf import settings
from auth.views import LoginRequiredView

from pluct import resource


class ListService(LoginRequiredView):
    def get(self, request):
        token = request.session.get('tsuru_token').replace('type ', '')
        auth = {
            'type': 'type',
            'credentials': token,
        }
        url = "{0}/services".format(settings.TSURU_HOST)
        services = resource.get(url, auth)
        return TemplateResponse(request, "services/list.html",
                                {'services': services})
