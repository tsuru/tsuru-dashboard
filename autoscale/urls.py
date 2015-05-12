from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'autoscale.views.index', name='autoscale'),
]
