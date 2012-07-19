import requests

from django.conf import settings
from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.views.generic.base import View
from auth.forms import TeamForm, LoginForm, SignupForm


def team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            response = requests.post('%s/teams' % settings.TSURU_HOST, dict(form.data))
            if response.status_code == 200:
                return HttpResponse("")
            else:
                return HttpResponse(response.content, status=response.status_code)
    context = {}
    context['form'] = TeamForm()
    return TemplateResponse(request, 'auth/team.html', context)


class Login(View):

	def get(self, request):
		return TemplateResponse(request, 'auth/login.html', context={'login_form': LoginForm()})

	def post(self, request):
		form = LoginForm(request.POST)
		if not form.is_valid():
			return TemplateResponse(request, 'auth/login.html', context={'login_form': form})


class Signup(View):

	def get(self, request):
		return TemplateResponse(request, 'auth/signup.html', context={'signup_form': SignupForm()})
