from django.conf.urls import url

from tsuru_autoscale.wizard import views


urlpatterns = [
    url(r'^(?P<instance>[\w-]+)/$', views.new, name='wizard-new'),
    url(r'^(?P<instance>[\w-]+)/remove/$', views.remove, name='wizard-remove'),
    url(r'^(?P<instance>[\w-]+)/enable/$', views.enable, name='wizard-enable'),
    url(r'^(?P<instance>[\w-]+)/disable/$', views.disable, name='wizard-disable'),
    url(r'^$', views.new, name='wizard-new'),
]
