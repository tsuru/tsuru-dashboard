from django.conf.urls import url

import views


urlpatterns = [
    url(r'^$', views.ListService.as_view(), name='service-list'),
    url(r'^(?P<service>[\w-]+)/instances/(?P<instance>[\w-]+)/$', views.ServiceInstanceDetail.as_view(),
        name='service-detail'),
    url(r'^(?P<service_name>[\w-]+)/add/$', views.ServiceAdd.as_view(),
        name='service-add'),
    url(r'^(?P<service>[\w-]+)/instances/(?P<instance>[\w-]+)/remove/$',
        views.ServiceRemove.as_view(), name='service-remove'),
    url(r'^(?P<service>[\w-]+)/instances/(?P<instance>[\w-]+)/bind/$', views.Bind.as_view(),
        name='bind'),
    url(r'^(?P<service>[\w-]+)/instances/(?P<instance>[\w-]+)/(?P<app>[\w-]+)/unbind/$',
        views.Unbind.as_view(), name='unbind'),
]
