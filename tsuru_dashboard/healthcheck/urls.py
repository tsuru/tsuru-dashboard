from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^$', "tsuru_dashboard.healthcheck.views.healthcheck", name='healthcheck'),
)
