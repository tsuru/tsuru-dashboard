from django.conf.urls import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from auth.views import Login


urlpatterns = patterns(
    '',
    url(r'^$', Login.as_view(), name='login'),

    (r'^auth/', include('auth.urls')),
    (r'^apps/', include('apps.urls')),
    (r'^services/', include('services.urls')),
)

urlpatterns += staticfiles_urlpatterns()
