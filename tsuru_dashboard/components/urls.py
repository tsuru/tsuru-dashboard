from django.conf.urls import url

import views


urlpatterns = [
    url(r'^$', views.ListComponent.as_view(), name='list-component'),
    url(r'^list.json$', views.ListComponentJson.as_view(), name='list-component-json')
]
