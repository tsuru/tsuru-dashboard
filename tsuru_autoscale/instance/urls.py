from django.conf.urls import url

from tsuru_autoscale.instance.views import ListInstance, InstanceInfo


urlpatterns = [
    url(r'^$', ListInstance.as_view(), name='instance-list'),
    url(r'^(?P<name>[\w-]+)/$', InstanceInfo.as_view(), name='instance-get'),
]
