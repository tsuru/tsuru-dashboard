from django.conf.urls import url, include

from tsuru_dashboard.dashboard.views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view()),
    url(r'^admin/', include('tsuru_dashboard.admin.urls')),
    url(r'^auth/', include('tsuru_dashboard.auth.urls')),
    url(r'^apps/', include('tsuru_dashboard.apps.urls')),
    url(r'^services/', include('tsuru_dashboard.services.urls')),
    url(r'^teams/', include('tsuru_dashboard.teams.urls')),
    url(r'^healthcheck/', include('tsuru_dashboard.healthcheck.urls')),
    url(r'^dashboard/', include('tsuru_dashboard.dashboard.urls')),
    url(r'^metrics/', include('tsuru_dashboard.metrics.urls')),
    url(r'^components/', include('tsuru_dashboard.components.urls')),
    url(r'^events/', include('tsuru_dashboard.events.urls')),
]
