from django.conf.urls import patterns, url

from admin_abyss import views

urlpatterns = patterns(
    '',
    url(r'^$', views.ListNode.as_view(), name='list-node'),
    url(r'^apps/(?P<appname>[\w-]+)/containers/$',
        views.ListContainersByApp.as_view(), name='list-containers-by-app'),
    url(r'^(?P<address>[\w.:1-9-]+)/containers/$',
        views.ListContainer.as_view(), name='list-container'),
    url(r'^deploys/$', views.ListDeploy.as_view(), name='list-deploys'),
    url(r'^deploys/graph$', views.DeploysGraph.as_view(),
        name='deploys-graph'),
    url(r'^(?P<deploy>[\s\w@\.-]+)/$', views.DeployInfo.as_view(), name='deploy-info'),
    url(r'^apps/$', views.ListAppAdmin.as_view(), name='list-app-admin'),
)
