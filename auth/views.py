from django.template.response import TemplateResponse

from auth.forms import LoginForm

def login(request):
    return TemplateResponse(request, 'auth/login.html', context={'login_form': LoginForm()})

def signup(request):
    return TemplateResponse(request, 'auth/signup.html')

