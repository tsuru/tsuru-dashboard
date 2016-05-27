from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt

import views

urlpatterns = patterns(
    '',
    url(r'^$', views.PoolList.as_view(), name='pool-list'),
    url(r'^pool/(?P<pool>[\w-]+)/$', views.PoolInfo.as_view(), name='pool-info'),
    url(r'^pool/(?P<pool>[\w-]+)/rebalance/$', csrf_exempt(views.PoolRebalance.as_view()),
        name='pool-rebalance'),
    url(r'^node/(?P<address>[http://\w.:1-9-]+)/remove/$', views.NodeRemove.as_view(),
        name='node-remove'),
    url(r'^node/add/$', csrf_exempt(views.NodeAdd.as_view()), name='node-add'),
    url(r'^deploys/$', views.ListDeploy.as_view(), name='list-deploys'),
    url(r'^deploys/(?P<deploy>[\s\w@\.-]+)/$', views.DeployInfo.as_view(), name='deploy-info'),
    url(r'^healing/$', views.ListHealing.as_view(), name='list-healing'),
    url(r'^templates.json$', views.TemplateListJson.as_view(), name='template-list-json'),
    url(r'^(?P<address>[http://\w.:1-9-]+)/containers/$', views.NodeInfoJson.as_view(),
        name='node-info-json'),
    url(r'^(?P<address>[http://\w.:1-9-]+)/$', views.NodeInfo.as_view(),
        name='node-info'),
)
