from django.conf.urls import patterns, include
from django.views.generic.base import RedirectView

import os


urlpatterns = patterns(
    '',
    (r'^$', RedirectView.as_view(url='/apps')),
    (r'^admin_abyss/', include('admin_abyss.urls')),
    (r'^auth/', include('auth.urls')),
    (r'^apps/', include('apps.urls')),
    (r'^services/', include('services.urls')),
    (r'^teams/', include('teams.urls')),
    (r'^quotas/', include('quotas.urls')),
    (r'^healthcheck/', include('healthcheck.urls')),
)

urlpatterns += patterns(
    '',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': os.path.join(os.path.dirname(__file__), 'static')})
)
