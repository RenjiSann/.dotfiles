from django import template
from django.db.models import QuerySet

from ..models.signup import ApplicationManager

register = template.Library()


@register.filter
def subtract(value, arg):
    return value - arg
