from django import template
from smartypants import smartypants

register = template.Library()

@register.filter
def smartquotes(text):
    return smartypants(text)

# Clean up text to match house style
# This might need to be marked as safe
@register.filter
def smartlines(text):
	text = smartypants(text)
	text = text.replace("<br /><br />","</p><p>")
	return text
