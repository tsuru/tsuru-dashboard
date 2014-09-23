from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^$', "healthcheck.views.healthcheck", name='healthcheck'),
)
