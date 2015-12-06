from django.http import HttpResponseRedirect

from tsuru_dashboard.auth.views import LoginRequiredView


class IndexView(LoginRequiredView):
    def get(self, request):
        return HttpResponseRedirect("/apps")
