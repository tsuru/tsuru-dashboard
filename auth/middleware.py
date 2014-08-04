from django.shortcuts import redirect
from django.core.urlresolvers import reverse

import logging

logger = logging.getLogger(__name__)


class VerifyToken(object):
    def process_exception(self, request, exception): 
        if isinstance(exception, Exception):
            logging.error(exception)
            return redirect(reverse("logout"))
