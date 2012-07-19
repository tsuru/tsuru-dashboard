from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('',
    url(r'^$', 'auth.views.login', name='login'),

    url(r'^login$', 'auth.views.login', name='login'),
    url(r'^signup$', 'auth.views.signup', name='signup'),
)


urlpatterns += staticfiles_urlpatterns()
