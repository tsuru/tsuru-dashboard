from django.conf.urls import patterns, url

import views


urlpatterns = patterns(
    '',
    url(r'^(?P<app_name>[\w-]+)/$', views.Metric.as_view(), name='metric'),
)
