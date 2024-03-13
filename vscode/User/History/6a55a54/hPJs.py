@register.filter
def match_event(things, category):
    return things.filter(category=category)