import json
import requests
from tsuruclient import client

from tsuru_dashboard import settings
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.contrib import messages

from .forms import (LoginForm, SignupForm, KeyForm, TokenRequestForm,
                    PasswordRecoveryForm, ChangePasswordForm)


def token_is_valid(token):
    headers = {'authorization': token}
    url = "{0}/users/info".format(settings.TSURU_HOST)
    response = requests.get(url, headers=headers)
    return response.status_code == 200


def get_permissions(token):
    headers = {"authorization": token}
    permissions = {}

    url = "{0}/users/info".format(settings.TSURU_HOST)
    response = requests.get(url, headers=headers)
    user = response.json()
    permissions["admin"] = False
    permissions["healing"] = False
    for perm in user["Permissions"]:
        if perm["Name"] == "" and perm["ContextType"] == "global":
            permissions["admin"] = True
            for k in permissions:
                permissions[k] = True
            return permissions
        elif perm["Name"] == "healing.read":
            permissions["healing"] = True

    return permissions


class LoginRequiredMixin(object):

    @property
    def client(self):
        target = settings.TSURU_HOST
        token = self.request.session.get('tsuru_token').split(" ")[-1]
        return client.Client(target, token)

    @property
    def authorization(self):
        return {'authorization': self.request.session.get('tsuru_token')}

    def dispatch(self, request, *args, **kwargs):
        token = request.session.get('tsuru_token')
        if not token or not token_is_valid(token):
            return redirect("%s?next=%s" % (reverse('login'), request.path))
        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class PermissionRequiredMixin(object):
    required_permission = "admin"

    def dispatch(self, request, *args, **kwargs):
        permission = request.session.get('permissions', {}).get(self.required_permission, False)
        if not permission:
            messages.error(self.request, u'Permission denied.', fail_silently=True)
            return redirect('/')
        else:
            return super(PermissionRequiredMixin, self).dispatch(
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
            messages.success(self.request, u'Password successfully updated!', fail_silently=True)
        else:
            messages.error(self.request, response.text, fail_silently=True)
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
        self.request.session["next_url"] = self.request.GET.get("next", "/apps")
        data = super(Login, self).get_context_data(*args, **kwargs)
        data["scheme_info"] = scheme = self.scheme_info()
        scheme_data = scheme.get('data', {})
        if scheme_data is None:
            return data
        authorize_url = scheme_data.get('authorizeUrl', '')
        callback_url = "http://{}/auth/callback/".format(self.request.META.get('HTTP_HOST'))
        data["authorize_url"] = authorize_url.replace('__redirect_url__', callback_url)
        return data

    def get_success_url(self):
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
            self.request.session['tsuru_token'] = "type {0}".format(result['token'])
            self.request.session['permissions'] = get_permissions(result['token'])
            return super(Login, self).form_valid(form)

        form.add_error(None, response.content)
        return super(Login, self).form_invalid(form)


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
        url = '{}/auth/login'.format(settings.TSURU_HOST)
        response = requests.post(url, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json()
            self.request.session['tsuru_token'] = "type {}".format(result['token'])
            self.request.session['permissions'] = get_permissions(result['token'])
            next_url = self.request.session["next_url"]
            return redirect(next_url)
        return redirect('/auth/login')


class KeyAdd(LoginRequiredMixin, FormView):
    form_class = KeyForm
    template_name = 'auth/key_add.html'
    success_url = '/auth/key/'

    def form_valid(self, form):
        url = '{}/users/keys'.format(settings.TSURU_HOST)
        response = requests.post(url, data=json.dumps(form.cleaned_data), headers=self.authorization)
        if response.status_code < 399:
            messages.success(self.request, "The key was successfully added", fail_silently=True)
        else:
            messages.error(self.request, response.text, fail_silently=True)
        return super(KeyAdd, self).form_valid(form)
