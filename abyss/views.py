from django.http import HttpResponseRedirect

from auth.views import LoginRequiredView


class IndexView(LoginRequiredView):
    def get(self, request):
        if not request.session.get("is_admin"):
            return HttpResponseRedirect("/apps")
        return HttpResponseRedirect("/dashboard")
