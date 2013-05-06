from django.conf.urls import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from auth.views import Login, Logout, Signup, Team, Key


urlpatterns = patterns(
    '',
    url(r'^$', Login.as_view(), name='login'),
    url(r'^login$', Login.as_view(), name='login'),
    url(r'^logout$', Logout.as_view(), name='logout'),
    url(r'^team/$', Team.as_view(), name='team'),
    url(r'^key/$', Key.as_view(), name='token'),
    url(r'^signup$', Signup.as_view(), name='signup'),

    (r'^apps/', include('apps.urls')),
    (r'^services/', include('services.urls')),
)

urlpatterns += staticfiles_urlpatterns()
