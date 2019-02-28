from django.conf.urls import url

from tsuru_autoscale.datasource import views

urlpatterns = [
    url(r'^$', views.list, name='datasource-list'),
    url(r'^new/$', views.new, name='datasource-new'),
    url(r'^(?P<name>[\w\s-]+)/remove/$', views.remove, name='datasource-remove'),
    url(r'^(?P<name>[\w\s-]+)/$', views.get, name='datasource-get'),
]
