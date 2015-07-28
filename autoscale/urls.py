from django.conf.urls import url

from autoscale.views import Index


urlpatterns = [
    url(r'^$', Index.as_view(), name='autoscale'),
]
