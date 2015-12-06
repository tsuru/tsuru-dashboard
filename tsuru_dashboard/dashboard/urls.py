from django.conf.urls import patterns, url
from django.views.decorators.cache import cache_page

import views

urlpatterns = patterns(
    '',
    url(r'^$', views.DashboardView.as_view(), name='dashboard'),
    url(r'^healing_status$', cache_page(60 * 5)(views.HealingView.as_view()), name='healing'),
    url(r'^cloud_status$', cache_page(60 * 30)(views.CloudStatusView.as_view()), name='cloud'),
    url(r'^deploys$', cache_page(60 * 5)(views.DeploysView.as_view()), name='deploys'),
)
