from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def signup_closed(event):
    return event.signup_end_date < timezone.now()

