from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt

import views


urlpatterns = patterns(
    '',
    url(r'^$', views.ListApp.as_view(), name='list-app'),
    url(r'^list.json$', views.ListAppJson.as_view(), name='list-app-json'),
    url(r'^create/$', views.CreateApp.as_view(), name='create-app'),
    url(r'^(?P<app_name>[\w-]+).json$',
        views.AppDetailJson.as_view(), name='detail-app-json'),
    url(r'^(?P<app_name>[\w-]+)/$',
        views.AppDetail.as_view(), name='detail-app'),
    url(r'^(?P<name>[\w-]+)/remove/$',
        views.RemoveApp.as_view(), name='remove_app'),
    url(r'^(?P<name>[\w-]+)/unlock/$', views.Unlock.as_view(), name='unlock-app'),
    url(r'^(?P<app_name>[\w-]+)/log/stream/$', views.LogStream.as_view(), name='app-log-stream'),
    url(r'^(?P<app_name>[\w-]+)/log/$', views.AppLog.as_view(),
        name='app_log'),
    url(r'^(?P<app_name>[\w-]+)/settings/$', views.Settings.as_view(),
        name='app-settings'),
    url(r'^(?P<app_name>[\w-]+)/deploys/$', csrf_exempt(views.ListDeploy.as_view()), name='app-deploys'),
    url(r'^(?P<app_name>[\w-]+)/deploys/(?P<deploy>[\s\w@\.-]+)/$',
        views.DeployInfo.as_view(), name='app-deploy'),
    url(r'^(?P<app_name>[\w-]+)/rollback/(?P<image>.+)/$',
        views.AppRollback.as_view(), name='app-rollback'),
)
