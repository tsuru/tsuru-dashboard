from django.conf.urls import patterns, url

import views


urlpatterns = patterns(
    '',
    url(r'^(?P<target_type>[\w-]+)/(?P<target_name>[\w-]+)/$', views.Metric.as_view(), name='metric'),
)
