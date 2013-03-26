from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from auth.views import Login, Logout, Signup, Team, Key
from apps.views import CreateApp, AppAddTeam, Run, ListApp, RemoveApp, AppLog, AppDetail, AppEnv, AppTeams

from django.views.generic.base import TemplateView, RedirectView

class TextPlainView(TemplateView):
    def render_to_response(self, context, **kwargs):
        return super(TextPlainView, self).render_to_response(
            context, content_type='text/plain', **kwargs)

urlpatterns = patterns('',
    url(r'^robots\.txt$', TextPlainView.as_view(template_name='robots.txt')),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),
    url(r'^$', Login.as_view(), name='login'),

    url(r'^login$', Login.as_view(), name='login'),
    url(r'^logout$', Logout.as_view(), name='logout'),
    url(r'^team/$', Team.as_view(), name='team'),
    url(r'^key/$', Key.as_view(), name='token'),
    url(r'^signup$', Signup.as_view(), name='signup'),

    url(r'^apps/$', ListApp.as_view(), name='list-app'),
    url(r'^apps/create/$', CreateApp.as_view(), name='create-app'),
    url(r'^app/run/$', Run.as_view(), name='run'),
    url(r'^app/(?P<app_name>[\w-]+)/$', AppDetail.as_view(), name='detail-app'),
    url(r'^app/(?P<name>[\w-]+)/remove/$', RemoveApp.as_view(), name='remove_app'),
    url(r'^app/(?P<app_name>[\w-]+)/log/$', AppLog.as_view(), name='app_log'),
    url(r'^app/(?P<app_name>[\w-]+)/env/$', AppEnv.as_view(), name='get-env'),
    url(r'^app/(?P<app_name>[\w-]+)/teams/$', AppTeams.as_view(), name='app-teams'),
    url(r'^app/(?P<app_name>[\w-]+)/team/add/$', AppAddTeam.as_view(), name='app-add-team'),
    url(r'^envs/$', "auth.views.env_vars", name='envs'),
)

urlpatterns += staticfiles_urlpatterns()
