from .models import events, signup

@register.filter
def match_event(application, category):
    return