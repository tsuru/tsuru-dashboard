from django.conf.urls import url, include
from django.contrib.staticfiles import views
from abyss import settings


urlpatterns = [
    url(r'^', include('tsuru_dashboard.urls')),
]

if settings.AUTOSCALE_HOST:
    urlpatterns += [url(r'^', include('tsuru_autoscale.urls'))]

urlpatterns += [url(r'^static/(?P<path>.*)$', views.serve)]
