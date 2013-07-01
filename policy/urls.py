from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^$', views.Policy.as_view(), name='policy'),
)
