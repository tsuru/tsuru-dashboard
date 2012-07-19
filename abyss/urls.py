from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'abyss.views.login', name='login'),
)
