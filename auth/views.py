import json
import requests

from django.conf import settings
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.views.generic.base import View

from auth.forms import TeamForm, LoginForm, SignupForm, KeyForm


class LoginRequiredView(View):

	def dispatch(self, request, *args, **kwargs):
		token = request.session.get('tsuru_token')
		if not token:
			return HttpResponseRedirect('/')
		return super(LoginRequiredView, self).dispatch(request, *args, **kwargs)


class Team(LoginRequiredView):

    def get(self, request):
        context = {}
        context['form'] = TeamForm()
        return TemplateResponse(request, 'auth/team.html', context)

    def post(self, request):
        form = TeamForm(request.POST)
        if form.is_valid():
            authorization = {'authorization': request.session.get('tsuru_token')}
            response = requests.post('%s/teams' % settings.TSURU_HOST,
                                     data=json.dumps(form.data),
                                     headers=authorization)
            if response.status_code == 200:
                return TemplateResponse(request, 'auth/team.html', {'form': form, 'message': "Time was successfully created"})
            else:
                return TemplateResponse(request, 'auth/team.html', {'form': form, 'errors': response.content})
        return TemplateResponse(request, 'auth/team.html', {'form': form, 'errors': form.errors})


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
				return HttpResponseRedirect("/team")
			context['msg'] = 'User not found'
		return TemplateResponse(request, 'auth/login.html', context=context)


class Logout(View):

    def get(self, request):
        if 'tsuru_token' in request.session:
            del request.session['tsuru_token']
        return HttpResponseRedirect('/')


class Signup(View):

    def get(self, request):
        return TemplateResponse(request, 'auth/signup.html', context={'signup_form': SignupForm()})

    def post(self, request):
        form = SignupForm(request.POST)
        if not form.is_valid():
            return TemplateResponse(request, 'auth/signup.html', context={'signup_form': form})
        post_data = {'email': form.data['email'], 'password' : form.data['password']}
        response = requests.post('%s/users' % settings.TSURU_HOST, data=json.dumps(post_data))
        if response.status_code == 201:
            return TemplateResponse(request, 'auth/signup.html', context={'signup_form': SignupForm(), 'message': 'User "%s" successfully created!' % form.data['email']})
        else:
            return TemplateResponse(request, 'auth/signup.html', context={'signup_form': form, 'error': response.content}, status=response.status_code)


class Key(LoginRequiredView):
    def get(self, request):
        context = {}
        context['form'] = KeyForm()
        return TemplateResponse(request, 'auth/key.html', context=context)

    def post(self, request):
        form = KeyForm(request.POST)
        if not form.is_valid():
            return TemplateResponse(request, 'auth/key.html', context={"form": form})

        authorization = {'authorization': request.session.get('tsuru_token')}
        response = requests.post('%s/users/keys' % settings.TSURU_HOST,
                                 data=json.dumps(request.POST),
                                 headers=authorization)

        if response.status_code == 200:
            return TemplateResponse(request, 'auth/key.html', context={"form": form, "message": "The Key was successfully added"})
        else:
            return TemplateResponse(request, 'auth/key.html', context={"form": form, "errors": response.content})

