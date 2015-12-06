from dateutil import parser
from django import template

import time

register = template.Library()


@register.filter
def string_to_date(value):
    deploy_date = parser.parse(value)
    return deploy_date


@register.filter
def time_to_string(value):
    return time.strftime('%Mm%Ss', time.gmtime(float(value)/1000000000))
