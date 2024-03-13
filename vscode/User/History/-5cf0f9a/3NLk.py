from django import template
from django.db.models import QuerySet

from ..models.signup import ApplicationManager, APPLICATION_STATUS

register = template.Library()


@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def any_accepted(applications):
    """
    Given a list of applications, return True if any of them is Confirmed
    """
    for app in applications:
        if app.status == APPLICATION_STATUS["CONFIRMED"]:
            return True
    return False

