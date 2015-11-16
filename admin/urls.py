from django.conf.urls import patterns, url
from django.views.decorators.cache import cache_page

from admin import views

urlpatterns = patterns(
    '',
    url(r'^$', cache_page(60 * 1)(views.PoolList.as_view()), name='pool-list'),
    url(r'^pool/(?P<pool>[\w-]+)/$', views.PoolInfo.as_view(), name='pool-info'),
    url(r'^(?P<address>[http://\w.:1-9-]+)/containers/$', views.NodeInfo.as_view(),
        name='node-info'),
    url(r'^node/(?P<address>[http://\w.:1-9-]+)/remove/$', views.NodeRemove.as_view(),
        name='node-remove'),
    url(r'^deploys/$', views.ListDeploy.as_view(), name='list-deploys'),
    url(r'^deploys/graph$', views.DeploysGraph.as_view(), name='deploys-graph'),
    url(r'^deploys/(?P<deploy>[\s\w@\.-]+)/$', views.DeployInfo.as_view(), name='deploy-info'),
    url(r'^healing/$', views.ListHealing.as_view(), name='list-healing'),
)
