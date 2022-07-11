from django import template

register = template.Library()


@register.filter(name="split")
def split(value, split_by):
    if not isinstance(value, str) or split_by not in value:
        return value
    return value.split(split_by)[0]
