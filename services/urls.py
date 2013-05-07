from django.conf.urls import patterns, url

from services import views


urlpatterns = patterns(
    '',
    url(r'^$', views.ListService.as_view(), name='service-list'),
    url(r'^(?P<service_name>[\w-]+)/$', views.ServiceDetail.as_view(),
        name='service-detail'),
    url(r'^(?P<service_name>[\w-]+)/add/$', views.ServiceAdd.as_view(),
        name='service-add'),
)
