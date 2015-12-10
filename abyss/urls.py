from django.conf.urls import url, include
import os



urlpatterns = [
    url(r'^', include('tsuru_dashboard.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(os.path.dirname(__file__), 'static')})
]
