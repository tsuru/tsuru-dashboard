from django.template.response import TemplateResponse

from auth.forms import TeamForm, LoginForm

def team(request):
    context = {}
    context['form'] = TeamForm()
    return TemplateResponse(request, 'auth/team.html', context)

def login(request):
    return TemplateResponse(request, 'auth/login.html', context={'login_form': LoginForm()})

def signup(request):
    return TemplateResponse(request, 'auth/signup.html')
