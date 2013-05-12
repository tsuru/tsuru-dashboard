from django.conf.urls import patterns, url

from auth import views


urlpatterns = patterns(
    '',
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', views.Logout.as_view(), name='logout'),
    url(r'^key/$', views.Key.as_view(), name='key'),
    url(r'^signup/$', views.Signup.as_view(), name='signup'),
)
