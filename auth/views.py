import json
import requests

from django.conf import settings
from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.views.generic.base import View
from auth.forms import TeamForm, LoginForm, SignupForm


class Team(View):
    def get(self, request):
        context = {}
        context['form'] = TeamForm()
        return TemplateResponse(request, 'auth/team.html', context)

    def post(self, request):
        form = TeamForm(request.POST)
        if form.is_valid():
            authorization = {'authorization': request.session.get('tsuru_token')}
            response = requests.post('%s/teams' % settings.TSURU_HOST, dict(form.data), headers=authorization)
            if response.status_code == 200:
                return HttpResponse("OK")
            else:
                return HttpResponse(response.content, status=response.status_code)
        return TemplateResponse(request, 'auth/team.html', {'form': form})


class Login(View):

	def get(self, request):
		return TemplateResponse(request, 'auth/login.html', context={'login_form': LoginForm()})

	def post(self, request):
		form = LoginForm(request.POST)
		context = {'login_form': form}
		if form.is_valid():
			username = form.data.get('username')
			data = {"password": form.data.get('password')}
			url = '%s/users/%s/tokens' % (settings.TSURU_HOST, username)
			response = requests.post(url, data=json.dumps(data))
			if response.status_code == 200:
				result = json.loads(response.text)
				request.session['tsuru_token'] = result['token']
				return HttpResponse("")
			context['msg'] = 'User not found'
		return TemplateResponse(request, 'auth/login.html', context=context)


class Signup(View):

    def get(self, request):
        return TemplateResponse(request, 'auth/signup.html', context={'signup_form': SignupForm()})
        
    def post(self, request):
        form = SignupForm(request.POST)
        if not form.is_valid():
            return TemplateResponse(request, 'auth/signup.html', context={'signup_form': form})
        
        post_data = {'email': form.data['email'], 'password' : form.data['password']}
        response = requests.post('%s/users' % settings.TSURU_HOST, data=json.dumps(post_data))
        
        if response.status_code == 200:
            return TemplateResponse(request, 'auth/signup.html', {'form': form, 'message': response.content})
        else:
            return TemplateResponse(request, 'auth/signup.html', {'form': form, 'error': response.content}, status=response.status_code)


