from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from auth.views import Login, Logout, Signup, Team, Key
from apps.views import CreateApp, AppAddTeam, Run, SetEnv, ListApp, RemoveApp, AppLog, AppDetail


urlpatterns = patterns('',
    url(r'^$', Login.as_view(), name='login'),

    url(r'^login$', Login.as_view(), name='login'),
    url(r'^logout$', Logout.as_view(), name='logout'),
    url(r'^team/$', Team.as_view(), name='team'),
    url(r'^key/$', Key.as_view(), name='token'),
    url(r'^signup$', Signup.as_view(), name='signup'),

    url(r'^app/$', ListApp.as_view(), name='list-app'),
    url(r'^app/(?P<app_name>[\w-]+)/$', AppDetail.as_view(), name='detail-app'),
    url(r'^app/(?P<name>[\w-]+)/remove/$', RemoveApp.as_view(), name='remove_app'),
    url(r'^app/(?P<name>[\w-]+)/log/$', AppLog.as_view(), name='app_log'),
    url(r'^app/create/$', CreateApp.as_view(), name='create-app'),
    url(r'^app/team/add/$', AppAddTeam.as_view(), name='app-add-team'),
    url(r'^app/run/$', Run.as_view(), name='run'),
    url(r'^app/env/set/$', SetEnv.as_view(), name='set-env'),
)

urlpatterns += staticfiles_urlpatterns()
