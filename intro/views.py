from django.views.generic.base import TemplateView


class Intro(TemplateView):
    template_name = 'intro/intro.html'
