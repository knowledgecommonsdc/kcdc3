from django import template
from smartypants import smartypants

register = template.Library()

@register.filter
def smartquotes(text):
    return smartypants(text)
