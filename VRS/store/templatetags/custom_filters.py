from django import template

register = template.Library()

@register.filter(name='split')
def split(value, sep):
    return value.split(sep)
