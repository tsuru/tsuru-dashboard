from django.views.generic.base import View
from django.template.response import TemplateResponse


class Apps(View):

    def get(self, request):
        return TemplateResponse(request, "apps/create.html")

