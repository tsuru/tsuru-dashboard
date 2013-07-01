from django.views.generic.base import TemplateView


class Policy(TemplateView):
    template_name = 'policy/policy.html'
