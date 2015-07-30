import os


def autoscale_enabled(request):
    context_extras = {}
    context_extras['autoscale_enabled'] = "AUTOSCALE_DASHBOARD_URL" in os.environ
    return context_extras
