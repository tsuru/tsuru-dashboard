from django.conf.urls import patterns, url

from services.views import ListService, ServiceDetail


urlpatterns = patterns(
    '',
    url(r'^$', ListService.as_view(), name='service-list'),
    url(r'^(?P<service_name>[\w-]+)/$', ServiceDetail.as_view(),
        name='service-detail'),
)
