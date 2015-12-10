from django.conf.urls import url, include
from django.conf import settings

import os


urlpatterns = [
    url(r'^', include('tsuru_dashboard.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(settings.BASE_DIR, 'static')})
]
