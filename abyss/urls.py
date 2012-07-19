from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'auth.views.login', name='login'),
    url(r'^login$', 'auth.views.login', name='login'),
)
