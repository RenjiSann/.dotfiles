from django import template
from ..models.signup import Application, ApplicationManager

register = template.Library()


@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def match_event(application, event_pk):
    if isinstance(application, (QuerySet, )):
        return application.filter(event=event_pk)
    else:
        return []
