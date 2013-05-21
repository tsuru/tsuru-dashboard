from django.conf.urls import patterns, url

from intro import views


urlpatterns = patterns(
    '',
    url(r'^$', views.Intro.as_view(), name='intro'),
)
