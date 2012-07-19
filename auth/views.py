from django.template.response import TemplateResponse

from auth.forms import TeamForm

def login(request):
    return TemplateResponse(request, 'auth/login.html')

def team(request):
    context = {}
    context['form'] = TeamForm()
    return TemplateResponse(request, 'auth/team.html', context)
