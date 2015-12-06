from django.conf.urls import url

from .views import Index


urlpatterns = [
    url(r'^(?P<app>[\w-]+)/$', Index.as_view(), name='autoscale'),
]
