from django.conf.urls import url

from tsuru_dashboard.healthcheck.views import healthcheck


urlpatterns = [
    url(r'^$', healthcheck, name='healthcheck'),
]
