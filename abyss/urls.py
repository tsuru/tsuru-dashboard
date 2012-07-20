from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from auth.views import Login, Logout, Signup, Team, Key
from apps.views import CreateApp, AppAddTeam


urlpatterns = patterns('',
    url(r'^$', Login.as_view(), name='login'),

    url(r'^login$', Login.as_view(), name='login'),
    url(r'^logout$', Logout.as_view(), name='logout'),
    url(r'^team/$', Team.as_view(), name='team'),
    url(r'^key/$', Key.as_view(), name='token'),
    url(r'^signup$', Signup.as_view(), name='signup'),

    url(r'^app/create/$', CreateApp.as_view(), name='create-app'),
    url(r'^app/team/add/$', AppAddTeam.as_view(), name='app-add-team'),
)

urlpatterns += staticfiles_urlpatterns()
