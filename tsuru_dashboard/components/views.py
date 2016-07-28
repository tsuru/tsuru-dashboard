from tsuru_dashboard.auth.views import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from tsuru_dashboard import settings


class ListComponentJson(LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, *args, **kwargs):
        component_list = {"components": [x.strip() for x in settings.METRICS_COMPONENTS.split(",")]}
        return JsonResponse(component_list, safe=False)


class ListComponent(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "components/list.html"
