from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.DashboardView.as_view(), name='dashboard'),
    url(r'^healing_status$', views.HealingView.as_view(), name='healing'),
    url(r'^cloud_status$', views.CloudStatusView.as_view(), name='cloud'),
    url(r'^deploys$', views.DeploysView.as_view(), name='deploys'),
]
