from django.conf.urls import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from quotas.views import Info


urlpatterns = patterns(
    '',
    url(r'^$', Info.as_view(), name='quota'),
    (r'^auth/', include('auth.urls')),
    (r'^apps/', include('apps.urls')),
    (r'^services/', include('services.urls')),
    (r'^teams/', include('teams.urls')),
)

urlpatterns += staticfiles_urlpatterns()
