from dateutil import parser
from django import template


register = template.Library()


@register.filter
def string_to_date(value):
    time = parser.parse("2014-02-27T17:55:34.2-03:00")
    return time