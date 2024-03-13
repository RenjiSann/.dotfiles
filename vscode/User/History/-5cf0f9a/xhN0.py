import datetime
from django import template

register = template.Library()


@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def signup_closed(event):
    return event.signup_end_date < 

