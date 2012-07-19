from django.template.response import TemplateResponse
from django.views.generic.base import View

from auth.forms import TeamForm, LoginForm, SignupForm


def team(request):
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