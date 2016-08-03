from dateutil import parser
from django import template

import time


register = template.Library()


@register.filter
def string_to_date(value):
    deploy_date = parser.parse(value)
    if deploy_date.year == 1:
        return None
    return deploy_date


@register.filter
def time_to_string(value):
    if value < 0:
        return ""
    t = time.gmtime(float(value) / (1000 * 1000 * 1000))
    fmt = '%Mm%Ss'
    if t.tm_hour > 0:
        fmt = '%Hh{}'.format(fmt)
    return time.strftime(fmt, t)
