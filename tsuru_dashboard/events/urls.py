from django.conf.urls import url

import views


urlpatterns = [
    url(r'^$', views.ListEvent.as_view(), name='event-list'),
    url(r'^(?P<uuid>[\w-]+)/$', views.EventInfo.as_view(), name='event-info'),
]
