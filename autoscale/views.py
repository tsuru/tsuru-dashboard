from django.views.generic import TemplateView

from auth.views import LoginRequiredMixin

import os
import urllib


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'autoscale/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Index, self).get_context_data(*args, **kwargs)
        token = self.request.session.get('tsuru_token').split(' ')[1]
        token = urllib.quote(token)
        app = kwargs["app"]

        service_url = "{}/app/{}?TSURU_TOKEN={}".format(
            os.environ.get("AUTOSCALE_DASHBOARD_URL"), app, token)

        context["service_url"] = service_url
        context["app"] = app
        return context
