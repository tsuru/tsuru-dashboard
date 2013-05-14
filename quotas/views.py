from django.template.response import TemplateResponse

from auth.views import LoginRequiredView


class Info(LoginRequiredView):
    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, "quota/info.html", {})
