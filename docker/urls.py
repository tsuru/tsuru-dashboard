from django.conf.urls import patterns, url

from docker import views

urlpatterns = patterns(
    '',
    url(r'^$', views.ListNode.as_view(), name='list-node'),
    url(r'^(?P<address>[\w.:1-9-]+)/containers/$',
        views.ListContainer.as_view(), name='list-container'),
)
