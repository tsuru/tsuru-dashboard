from django.conf.urls import patterns, url

import views


urlpatterns = patterns(
    '',
    url(r'^$', views.ListComponent.as_view(), name='list-component'),
    url(r'^list.json$', views.ListComponentJson.as_view(), name='list-component-json')
)
