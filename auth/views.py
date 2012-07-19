from django.template.response import TemplateResponse

def login(request):
    return TemplateResponse(request, 'auth/login.html')

def signup(request):
    return TemplateResponse(request, 'auth/signup.html')