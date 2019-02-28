from django.conf.urls import url

from tsuru_autoscale.app import views

urlpatterns = [
    url(r'^apps/(?P<app>[\w-]+)/autoscale/$', views.AutoScale.as_view(), name='autoscale-app-info'),
]
