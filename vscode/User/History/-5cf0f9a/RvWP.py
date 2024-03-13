from django import template
from django.utils import timezone
from django.utils.formats import date_format
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
        fmt_signup_start = date_format(event.signup_start_date, "D F Y")
        return f"Les inscriptions ouvriront le {fmt_signup_start}."
