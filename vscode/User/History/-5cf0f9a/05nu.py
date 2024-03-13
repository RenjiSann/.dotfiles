from django import template
from django.utils import timezone
from django.utils.formats import date_format
from django.utils.translation import gettext_lazy as _
from django.db.models import QuerySet

from ..models.signup import APPLICATION_STATUS, ApplicationManager

register = template.Library()


@register.filter
def subtract(value, arg):
    return value - arg
@register.filter
def event_format(event):
    duration = event.end_date - event.start_date
    return "week" if duration.days > 2 else "weekend"


@register.filter
def signup_finished(event):
    return event.signup_end_date < timezone.now()


@register.filter
def signup_not_yet_opened(event):
    return event.signup_start_date > timezone.now()


@register.filter
def signup_opened(event):
    return not (signup_finished(event) or signup_not_yet_opened(event))


@register.filter
def is_finished(event):
    return event.end_date < timezone.now()


@register.filter
def signup_status_string(event):
    # Inscriptions finies
    if signup_finished(event):
        return "Les inscriptions pour ce stage sont fermées."
    # Inscriptions pas encore ouvertes
    elif signup_not_yet_opened(event):
        fmt_signup_start = date_format(event.signup_start_date, "d F Y")
        return f"Les inscriptions ouvriront le {fmt_signup_start}."
    else:
        return "Les inscriptions pour ce stage sont ouvertes."


@register.filter
def match_event(application, event_pk):
    if isinstance(application, (QuerySet, ApplicationManager)):
        return application.filter(event=event_pk)
    else:
        return []


@register.filter
def any_confirmed(applications):
    """
    Given a list of applications, return True if any of them is Confirmed
    """
    for app in applications:
        if app.status == APPLICATION_STATUS["CONFIRMED"]:
            return True
    return False
