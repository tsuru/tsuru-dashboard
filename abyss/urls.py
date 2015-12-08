import os

from django.conf.urls import patterns, include

from tsuru_dashboard.dashboard.views import IndexView

urlpatterns = patterns(
    '',
    (r'^$', IndexView.as_view()),
    (r'^admin/', include('tsuru_dashboard.admin.urls')),
    (r'^auth/', include('tsuru_dashboard.auth.urls')),
    (r'^apps/', include('tsuru_dashboard.apps.urls')),
    (r'^services/', include('tsuru_dashboard.services.urls')),
    (r'^teams/', include('tsuru_dashboard.teams.urls')),
    (r'^healthcheck/', include('tsuru_dashboard.healthcheck.urls')),
    (r'^autoscale/', include('tsuru_dashboard.autoscale.urls')),
    (r'^dashboard/', include('tsuru_dashboard.dashboard.urls')),
    (r'^metrics/', include('tsuru_dashboard.metrics.urls')),
)

urlpatterns += patterns(
    '',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': os.path.join(os.path.dirname(__file__), 'static')})
)
