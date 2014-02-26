from django.conf.urls import patterns, url

from docker import views

urlpatterns = patterns(
    '',
    url(r'^$', views.ListNode.as_view(), name='list-node'),
    url(r'^$', views.ListContainer.as_view(), name='list-container'),
)
