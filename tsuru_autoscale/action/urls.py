from django.conf.urls import url

from tsuru_autoscale.action import views


urlpatterns = [
    url(r'^new/$', views.new, name='action-new'),
    url(r'^(?P<name>[\w\s-]+)/remove/$', views.remove, name='action-remove'),
    url(r'^(?P<name>[\w\s-]+)/$', views.get, name='action-get'),
    url(r'^$', views.list, name='action-list'),
]
