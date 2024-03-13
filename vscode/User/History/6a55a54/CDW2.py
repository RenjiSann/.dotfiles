from .models import events, signup

@register.filter
def match_event(application, event_pk):
    return application.filter()