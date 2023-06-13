from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.DashboardView.as_view(), name='dashboard'),
    url(r'^cloud_status$', views.CloudStatusView.as_view(), name='cloud'),
    url(r'^deploys$', views.DeploysView.as_view(), name='deploys'),
]
