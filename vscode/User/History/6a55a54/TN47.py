@register.filter
def in_category(things, category):
    return things.filter(category=category)