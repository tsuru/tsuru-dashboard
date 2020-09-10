from django import template

register = template.Library()


@register.filter
def divide(value, arg):
    try:
        return "%g" % (float(value) / int(arg))
    except (ValueError, ZeroDivisionError):
        return None
