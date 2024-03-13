from django import template
from django.db.models import QuerySet

from ..models.signup import ApplicationManager

register = template.Library()


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def get_event(application, event_pk):
    if isinstance(application, (QuerySet, ApplicationManager)):
        return application.filter(event=event_pk)
    else:
        return []
