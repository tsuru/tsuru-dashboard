from tsuru_dashboard.auth.views import LoginRequiredView, LoginRequiredMixin
from django.views.generic import TemplateView
from django.http import JsonResponse


class ListComponentJson(LoginRequiredView):
    def get(self, *args, **kwargs):
        component_list = {"components": ["registry", "big-sibling"]}
        return JsonResponse(component_list, safe=False)


class ListComponent(LoginRequiredMixin, TemplateView):
    template_name = "components/list.html"
