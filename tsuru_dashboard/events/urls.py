from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

import views


urlpatterns = [
    url(r'^$', views.ListEvent.as_view(), name='event-list'),
    url(r'^kinds/$', views.KindList.as_view(), name='kind-list'),
    url(r'^(?P<uuid>[\w-]+)/$', views.EventInfo.as_view(), name='event-info'),
    url(r'^(?P<uuid>[\w-]+)/cancel/$', csrf_exempt(views.EventCancel.as_view()), name='event-cancel'),
]
