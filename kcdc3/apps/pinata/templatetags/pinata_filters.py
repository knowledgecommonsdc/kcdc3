from django import template
from smartypants import smartypants

register = template.Library()

@register.filter
def smartquotes(text):
    return smartypants(text)

# This might need to be marked as safe
@register.filter
def remove_double_linebreaks(text):
    return text.replace("<br /><br />","</p><p>")

