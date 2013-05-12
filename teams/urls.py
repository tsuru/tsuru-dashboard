from django.conf.urls import patterns, url

from teams import views


urlpatterns = patterns(
    '',
    url(r'^$', views.List.as_view(), name='team-list'),
    url(r'^(?P<team>[\w-]+)/remove/$', views.Remove.as_view(),
        name='team-remove'),
)
