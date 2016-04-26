from tsuru_dashboard.auth.views import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView, View
from django.http import JsonResponse


class ListComponentJson(LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, *args, **kwargs):
        component_list = {"components": ["registry", "big-sibling"]}
        return JsonResponse(component_list, safe=False)


class ListComponent(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "components/list.html"
