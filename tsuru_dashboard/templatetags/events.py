from django import template
from django.urls import reverse


register = template.Library()


@register.simple_tag
def event_url(event_id, app_name=''):
    if app_name != '':
        return reverse('app-event', args=[app_name, event_id])
    return reverse('event-info', args=[event_id])
