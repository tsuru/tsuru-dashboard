from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from auth.views import Login, Signup

urlpatterns = patterns('',
    url(r'^$', Login.as_view(), name='login'),

    url(r'^login$', Login.as_view(), name='login'),
    url(r'^team/$', 'auth.views.team', name='team'),
    url(r'^signup$', Signup.as_view(), name='signup'),
)


urlpatterns += staticfiles_urlpatterns()
