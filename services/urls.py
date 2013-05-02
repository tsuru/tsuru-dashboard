from django.conf.urls import patterns, url

from services.views import ListService


urlpatterns = patterns(
    '',
    url(r'^$', ListService.as_view(), name='service-list'),
)
