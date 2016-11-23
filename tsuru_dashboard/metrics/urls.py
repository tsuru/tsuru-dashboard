from django.conf.urls import url

import views


urlpatterns = [
    url(r'^app/(?P<target>[\w-]+)/$', views.AppMetric.as_view(), name='app-metric'),
    url(r'^component/(?P<target>[\w-]+)/$', views.ComponentMetric.as_view(), name='component-metric'),
    url(r'^node/(?P<target>[\w.-]+)/$', views.NodeMetric.as_view(), name='node-metric'),
    url(r'^pool/(?P<target>[\w-]+)/$', views.PoolMetric.as_view(), name='pool-metric')
]
