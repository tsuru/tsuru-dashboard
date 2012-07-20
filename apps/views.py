import json
import requests

from django.views.generic.base import View
from django.template.response import TemplateResponse
from django.conf import settings

from apps.forms import AppForm


class CreateApp(View):

    def get(self, request):
        return TemplateResponse(request, "apps/create.html", {"app_form": AppForm()})

    def post(self, request):
        form = AppForm(request.POST)
        if form.is_valid():
            authorization = {'authorization': request.session.get('tsuru_token')}
            data = form.data
            data.update({"framework": "django"})
            response = requests.post('%s/apps' % settings.TSURU_HOST,
                                     data=json.dumps(form.data),
                                     headers=authorization)
            if response.status_code == 200:
                return TemplateResponse(request, 'apps/create.html', {'form': form, 'message': "App was successfully created"})
            return TemplateResponse(request, 'apps/create.html', {'form': form, 'error': response.content})
        return TemplateResponse(request, 'apps/create.html', {'form': form})
