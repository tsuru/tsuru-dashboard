from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('tsuru_dashboard.urls')),
]
