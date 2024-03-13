from django import template

register = template.Library()


@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def match_event(application, event_pk):
    return application.filter(event=event_pk)
