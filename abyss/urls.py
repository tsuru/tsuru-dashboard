import os

from django.conf.urls import patterns, include

from abyss.views import IndexView

urlpatterns = patterns(
    '',
    (r'^$', IndexView.as_view()),
    (r'^admin/', include('admin.urls')),
    (r'^auth/', include('auth.urls')),
    (r'^apps/', include('apps.urls')),
    (r'^services/', include('services.urls')),
    (r'^teams/', include('teams.urls')),
    (r'^quotas/', include('quotas.urls')),
    (r'^healthcheck/', include('healthcheck.urls')),
    (r'^autoscale/', include('autoscale.urls')),
    (r'^dashboard/', include('dashboard.urls')),
)

urlpatterns += patterns(
    '',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': os.path.join(os.path.dirname(__file__), 'static')})
)
