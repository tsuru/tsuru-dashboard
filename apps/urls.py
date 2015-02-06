from django.conf.urls import patterns, url

from apps import views


urlpatterns = patterns(
    '',
    url(r'^$', views.ListApp.as_view(), name='list-app'),
    url(r'^create/$', views.CreateApp.as_view(), name='create-app'),
    url(r'^run/$', views.Run.as_view(), name='run'),
    url(r'^(?P<app_name>[\w-]+)/$',
        views.AppDetail.as_view(), name='detail-app'),
    url(r'^(?P<name>[\w-]+)/remove/$',
        views.RemoveApp.as_view(), name='remove_app'),
    url(r'^(?P<app_name>[\w-]+)/log/$', views.AppLog.as_view(),
        name='app_log'),
    url(r'^(?P<app_name>[\w-]+)/env/$', views.AppEnv.as_view(),
        name='get-env'),
    url(r'^(?P<app_name>[\w-]+)/teams/$',
        views.AppTeams.as_view(), name='app-teams'),
    url(r'^(?P<app_name>[\w-]+)/team/add/$',
        views.AppAddTeam.as_view(), name='app-add-team'),
    url(r'^(?P<app_name>[\w-]+)/team/revoke/(?P<team>[\w-]+)',
        views.AppRevokeTeam.as_view(), name='app-revoke-team'),
    url(r'^(?P<app_name>[\w-]+)/units/$',
        views.ChangeUnit.as_view(), name='change-units'),
    url(r'^(?P<app_name>[\w-]+)/metrics/$',
        views.MetricDetail.as_view(), name='metrics-app'),
    url(r'^(?P<app_name>[\w-]+)/autoscale/$', views.AutoscaleDetail.as_view(), name='autoscale-app'),
    url(r'^(?P<app_name>[\w-]+)/autoscale/enable/$', views.AutoscaleEnable.as_view(), name='autoscale-enable'),
    url(r'^(?P<app_name>[\w-]+)/deploys/$', views.ListDeploy.as_view(), name='app-deploys'),
    url(r'^(?P<app_name>[\w-]+)/deploys/(?P<deploy>[\s\w@\.-]+)/$',
        views.DeployInfo.as_view(), name='app-deploy'),
)
