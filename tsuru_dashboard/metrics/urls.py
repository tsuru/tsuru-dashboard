from django.conf.urls import patterns, url

import views


urlpatterns = patterns(
    '',
    url(r'^app/(?P<name>[\w-]+)/$', views.AppMetric.as_view(), name='app-metric'),
    url(r'^component/(?P<name>[\w-]+)/$', views.ComponentMetric.as_view(), name='component-metric')
)
