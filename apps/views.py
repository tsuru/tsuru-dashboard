from django.views.generic.base import View
from django.template.response import TemplateResponse

from apps.forms import AppForm


class CreateApp(View):

    def get(self, request):
        return TemplateResponse(request, "apps/create.html", {"app_form": AppForm()})
