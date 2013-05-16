import json
import requests

from django.conf import settings
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormView

from django.core.urlresolvers import reverse

from auth.forms import (LoginForm, SignupForm, KeyForm, TokenRequestForm,
                        PasswordRecoveryForm)


class LoginRequiredView(View):
    def dispatch(self, request, *args, **kwargs):
        token = request.session.get('tsuru_token')
        if not token:
            return redirect(reverse('login'))
        return super(LoginRequiredView, self).dispatch(
            request, *args, **kwargs)


class TokenRequest(FormView):
    template_name = 'auth/token_request.html'
    form_class = TokenRequestForm
    success_url = '/auth/token-request/success/'

    def form_valid(self, form):
        form.send()
        return super(TokenRequest, self).form_valid(form)


class TokenRequestSuccess(TemplateView):
    template_name = 'auth/token_request_success.html'


class PasswordRecoverySuccess(TemplateView):
    template_name = 'auth/password_recovery_success.html'


class PasswordRecovery(FormView):
    template_name = 'auth/password_recovery.html'
    form_class = PasswordRecoveryForm
    success_url = '/'

    def form_valid(self, form):
        form.send()
        return super(PasswordRecovery, self).form_valid(form)


class Login(View):

    def get(self, request):
        return TemplateResponse(request, 'auth/login.html',
                                context={'login_form': LoginForm()})

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
                request.session['username'] = username
                request.session['tsuru_token'] = "type {0}".format(
                    result['token'])
                return redirect("/apps")
            context['msg'] = 'User not found'
        return TemplateResponse(request, 'auth/login.html',
                                context=context)


class Logout(View):

    def get(self, request):
        if 'tsuru_token' in request.session:
            del request.session['tsuru_token']
        return redirect('/')


class Signup(View):

    def get(self, request):
        return TemplateResponse(request, 'auth/signup.html',
                                context={'signup_form': SignupForm()})

    def post(self, request):
        form = SignupForm(request.POST)
        if not form.is_valid():
            return TemplateResponse(request,
                                    'auth/signup.html',
                                    context={'signup_form': form})
        post_data = {'email': form.data['email'],
                     'password': form.data['password']}
        response = requests.post(
            '%s/users' % settings.TSURU_HOST,
            data=json.dumps(post_data))
        if response.status_code == 201:
            message = 'User "{0}" successfully created!'.format(
                form.data['email']
            )
            return TemplateResponse(request, 'auth/signup.html',
                                    context={'signup_form': SignupForm(),
                                             'message': message})
        else:
            return TemplateResponse(request, 'auth/signup.html',
                                    context={'signup_form': form,
                                             'error': response.content},
                                    status=response.status_code)


class Key(LoginRequiredView):
    def get(self, request):
        context = {}
        context['form'] = KeyForm()
        return TemplateResponse(request, 'auth/key.html', context=context)

    def post(self, request):
        form = KeyForm(request.POST)
        if not form.is_valid():
            return TemplateResponse(request, 'auth/key.html',
                                    context={"form": form})

        authorization = {'authorization': request.session.get('tsuru_token')}
        response = requests.post('%s/users/keys' % settings.TSURU_HOST,
                                 data=json.dumps(request.POST),
                                 headers=authorization)

        if response.status_code == 200:
            message = "The Key was successfully added"
            return TemplateResponse(request, 'auth/key.html',
                                    context={"form": form,
                                             "message": message})
        else:
            return TemplateResponse(request, 'auth/key.html',
                                    context={"form": form,
                                             "errors": response.content})
