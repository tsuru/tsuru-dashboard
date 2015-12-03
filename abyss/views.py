from django.http import HttpResponseRedirect

from auth.views import LoginRequiredView


class IndexView(LoginRequiredView):
    def get(self, request):
        return HttpResponseRedirect("/apps")
