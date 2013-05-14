from django.template.response import TemplateResponse
from django.conf import settings

from auth.views import LoginRequiredView

import requests


class Info(LoginRequiredView):
    def get(self, request, *args, **kwargs):
        headers = {'authorization': self.request.session.get('tsuru_token')}
        url = "{0}/quota/{1}".format(settings.TSURU_HOST,
                                     request.session["username"])
        response = requests.get(url, headers=headers)
        if response.status_code > 399:
            data = None
        else:
            data = response.json()
        context = {
            'quota': data
        }
        return TemplateResponse(request, "quota/info.html", context)
