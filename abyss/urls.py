from django.conf.urls import url, include
from django.contrib.staticfiles import views
from abyss import settings


urlpatterns = [
    url(r'^', include('tsuru_dashboard.urls')),
    url(r'^', include('tsuru_autoscale.urls')),
    url(r'^static/(?P<path>.*)$', views.serve),
]