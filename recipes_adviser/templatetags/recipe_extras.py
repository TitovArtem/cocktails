from django import template

register = template.Library()


@register.filter(name='item')
def item(dict, key):
    return dict[key]
