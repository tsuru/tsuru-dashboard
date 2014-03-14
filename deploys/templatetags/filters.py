from dateutil import parser
from django import template

import time

register = template.Library()


@register.filter
def string_to_date(value):
    deploy_date = parser.parse("2014-02-27T17:55:34.2-03:00")
    return deploy_date


@register.filter
def string_to_time(value):
    return time.strftime('%Mm%Ss', time.gmtime(float(value)/1000000000))
