from django import template
from django.db.models import QuerySet

from ..models.signup import ApplicationManager

register = template.Library()


@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def any_accepted(applications):
    """
    Given a list of applications, return True if any of them is Confirmed
    """
    
