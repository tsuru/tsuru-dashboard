import json
import requests

from django.conf import settings
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.contrib import messages

from auth.forms import (LoginForm, SignupForm, KeyForm, TokenRequestForm,
                        PasswordRecoveryForm, ChangePasswordForm)

from intro.models import Intro


class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        token = request.session.get('tsuru_token')
        if not token:
            return redirect(reverse('login'))
        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class ChangePassword(LoginRequiredMixin, FormView):
    template_name = 'auth/change_password.html'
    form_class = ChangePasswordForm
    success_url = '/auth/change-password/'

    def form_valid(self, form):
        data = form.cleaned_data
        headers = {'authorization': self.request.session.get('tsuru_token')}
        url = "{0}/users/password".format(settings.TSURU_HOST)
        response = requests.put(url, data=json.dumps(data), headers=headers)
        if response.status_code < 399:
            messages.success(self.request, u'Password successfully updated!')
        else:
            messages.error(self.request, response.text)
        return super(ChangePassword, self).form_valid(form)


class LoginRequiredView(LoginRequiredMixin, View):
    pass


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
    success_url = '/auth/password-recovery/success/'

    def form_valid(self, form):
        form.send()
        return super(PasswordRecovery, self).form_valid(form)


class Login(FormView):
    template_name = 'auth/login.html'
    form_class = LoginForm

    def get_context_data(self, *args, **kwargs):
        data = super(Login, self).get_context_data(*args, **kwargs)
        data["scheme_info"] = scheme = self.scheme_info()
        authorize_url = scheme.get('data', {}).get('authorizeUrl', '')
        callback_url = "http://{}/auth/callback/".format(self.request.META.get('HTTP_HOST'))
        data["authorize_url"] = authorize_url.replace('__redirect_url__', callback_url)
        return data

    def get_success_url(self):
        if hasattr(settings, "INTRO_ENABLED") and settings.INTRO_ENABLED:
            _, created = Intro.objects.get_or_create(
                email=self.request.session['username'])
            if created:
                return '/intro'
        return '/apps'

    def scheme_info(self):
        url = '{0}/auth/scheme'.format(settings.TSURU_HOST)
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return {}

    def form_valid(self, form):
        username = form.cleaned_data['username']
        data = {"password": form.cleaned_data['password']}
        url = '{0}/users/{1}/tokens'.format(settings.TSURU_HOST, username)
        response = requests.post(url, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json()
            self.request.session['username'] = username
            self.request.session['tsuru_token'] = "type {0}".format(
                result['token'])
            self.request.session['is_admin'] = result.get('is_admin', False)
            return super(Login, self).form_valid(form)
        return redirect('/auth/login')


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


class Callback(View):
    def get(self, request):
        code = request.GET.get("code")
        redirect_url = "http://{}/auth/callback/".format(request.META.get('HTTP_HOST'))
        data = {
            "code": code,
            "redirectUrl": redirect_url,
        }
        url = '{0}/auth/login'.format(settings.TSURU_HOST)
        response = requests.post(url, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json()
            self.request.session['tsuru_token'] = "type {0}".format(
                result['token'])
            self.request.session['is_admin'] = result.get('is_admin', False)
            return redirect('/apps')
        return redirect('/auth/login')


class Key(LoginRequiredMixin, FormView):
    form_class = KeyForm
    template_name = 'auth/key.html'
    success_url = '/auth/key/'

    def form_valid(self, form):
        authorization = {'authorization':
                         self.request.session.get('tsuru_token')}
        response = requests.post('%s/users/keys' % settings.TSURU_HOST,
                                 data=json.dumps(form.cleaned_data),
                                 headers=authorization)
        if response.status_code < 399:
            messages.success(self.request, "The key was successfully added")
        else:
            messages.error(self.request, response.text)
        return super(Key, self).form_valid(form)
