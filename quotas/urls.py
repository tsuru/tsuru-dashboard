from django.conf.urls import patterns, url

from quotas import views


urlpatterns = patterns(
    '',
    url(r'^$', views.Info.as_view(), name='quota'),
)
