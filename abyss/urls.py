from django.conf.urls import patterns, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns(
    '',
    (r'^auth/', include('auth.urls')),
    (r'^apps/', include('apps.urls')),
    (r'^services/', include('services.urls')),
    (r'^teams/', include('teams.urls')),
    (r'^quotas/', include('quotas.urls')),
)

urlpatterns += staticfiles_urlpatterns()
