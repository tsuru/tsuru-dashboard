from django.conf.urls import patterns, url

from deploys import views

urlpatterns = patterns(
    '',
    url(r'^$', views.ListDeploy.as_view(), name='list-deploys'),
)
