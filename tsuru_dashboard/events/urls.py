from django.conf.urls import url

import views


urlpatterns = [
    url(r'^$', views.ListEvent.as_view(), name='event-list'),
    url(r'^kinds/$', views.KindList.as_view(), name='kind-list'),
    url(r'^(?P<uuid>[\w-]+)/$', views.EventInfo.as_view(), name='event-info'),
    url(r'^(?P<uuid>[\w-]+)/cancel/$', views.EventCancel.as_view(), name='event-cancel'),
]
