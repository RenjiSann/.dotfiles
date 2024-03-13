from django import template
from ..models.signup import Application

register = template.Library()


@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def match_event(application, event_pk):
    if isinstance(application, Application):
        return application.filter(event=event_pk)
    else:
        return []
