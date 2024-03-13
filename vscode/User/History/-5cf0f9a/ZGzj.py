from django import template
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

register = template.Library()


@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def signup_closed(event):
    return event.signup_end_date < timezone.now()

@register.filter
def signup_status_string(event):
    # Inscriptions finies
    if event.signup_end_date < timezone.now():
        return "Les inscriptions pour ce stage sont fermées."
    # Inscriptions pas encore ouvertes
    elif event.signup_start_date > timezone.now():
        return "Les inscriptions ouvriront le."
