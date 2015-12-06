from django.conf.urls import patterns, url

import views


urlpatterns = patterns(
    '',
    url(r'^$', views.List.as_view(), name='team-list'),
    url(r'^(?P<team>[\s\w@\.-]+)/remove/$', views.Remove.as_view(),
        name='team-remove'),
    url(r'^add/$', views.Add.as_view(),
        name='team-add'),
    url(r'^(?P<team>[\s\w@\.-]+)/user/add/$', views.AddUser.as_view(),
        name='team-user-add'),
    url(r'^(?P<team>[\s\w@\.-]+)/user/(?P<user>.*)/remove/$',
        views.RemoveUser.as_view(), name='team-user-remove'),
    url(r'^(?P<team>[\s\w@\.-]+)/$', views.Info.as_view(), name='team-info'),
)
