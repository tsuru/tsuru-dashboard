from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.conf import settings

import logging

logger = logging.getLogger('dashboard')


class VerifyToken(object):
    def process_exception(self, request, exception):
        if not settings.DEBUG:
            if isinstance(exception, Exception):
                logger.error(exception)
                return redirect(reverse("logout"))
