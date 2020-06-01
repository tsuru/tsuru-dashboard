from django.conf.urls import url

import views


urlpatterns = [
    url(r'^$', views.ListApp.as_view(), name='list-app'),
    url(r'^list.json$', views.ListAppJson.as_view(), name='list-app-json'),
    url(r'^create/$', views.CreateApp.as_view(), name='create-app'),
    url(r'^(?P<app_name>[\w-]+).json$',
        views.AppDetailJson.as_view(), name='detail-app-json'),
    url(r'^(?P<app_name>[\w-]+)/$',
        views.AppResources.as_view(), name='app-resources'),
    url(r'^(?P<app_name>[\w-]+)/info/$',
        views.AppInfo.as_view(), name='app-info'),
    url(r'^(?P<name>[\w-]+)/remove/$',
        views.RemoveApp.as_view(), name='remove_app'),
    url(r'^(?P<name>[\w-]+)/unlock/$', views.Unlock.as_view(), name='unlock-app'),
    url(r'^(?P<app_name>[\w-]+)/log/stream/$', views.LogStream.as_view(), name='app-log-stream'),
    url(r'^(?P<app_name>[\w-]+)/log/$', views.AppLog.as_view(),
        name='app-log'),
    url(r'^(?P<app_name>[\w-]+)/settings/$', views.Settings.as_view(),
        name='app-settings'),
    url(r'^(?P<app_name>[\w-]+)/deploys/$', views.ListDeploy.as_view(), name='app-deploys'),
    url(r'^(?P<app_name>[\w-]+)/deploys/(?P<deploy>[\s\w@\.-]+)/$',
        views.DeployInfo.as_view(), name='app-deploy'),
    url(r'^(?P<app_name>[\w-]+)/rollback/(?P<image>.+)/$',
        views.AppRollback.as_view(), name='app-rollback'),
    url(r'^(?P<app_name>[\w-]+)/events/$', views.EventList.as_view(), name='app-events'),
    url(r'^(?P<app_name>[\w-]+)/events/(?P<uuid>[\s\w@\.-]+)/$',
        views.EventInfo.as_view(), name='app-event'),
]
