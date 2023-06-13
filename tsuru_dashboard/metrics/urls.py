from django.conf.urls import url

import views


urlpatterns = [
    url(r'^app/(?P<target>[\w-]+)/$', views.AppMetric.as_view(), name='app-metric'),
]
