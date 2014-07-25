from django.shortcuts import redirect
from django.core.urlresolvers import reverse


class VerifyToken(object):
    def process_exception(self, request, exception): 
        if isinstance(exception, Exception):
            return redirect(reverse("logout"))
