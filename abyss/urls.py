from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from auth.views import Login, Logout, Signup, Team
from apps.views import Apps

urlpatterns = patterns('',
    url(r'^$', Login.as_view(), name='login'),

    url(r'^login$', Login.as_view(), name='login'),
    url(r'^logout$', Logout.as_view(), name='logout'),
    url(r'^team/$', Team.as_view(), name='team'),
    url(r'^signup$', Signup.as_view(), name='signup'),

    url(r'^apps/$', Apps.as_view(), name='apps'),
)

urlpatterns += staticfiles_urlpatterns()
