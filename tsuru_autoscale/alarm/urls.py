from django.conf.urls import url

from tsuru_autoscale.alarm import views
from tsuru_autoscale.event.views import list as event_list

urlpatterns = [
    url(r'^$', views.list, name='alarm-list'),
    url(r'^new/$', views.new, name='alarm-new'),
    url(r'^(?P<name>[\w\s-]+)/remove/$', views.remove, name='alarm-remove'),
    url(r'^(?P<alarm_name>[\w\s-]+)/event/$', event_list, name='event-list'),
    url(r'^(?P<name>[\w\s-]+)/$', views.get, name='alarm-get'),
]
