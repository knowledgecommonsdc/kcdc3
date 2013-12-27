from django import template
from smartypants import smartypants
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def smartquotes(text):
    return smartypants(text)

# Clean up text to match house style
#
# We are marking the results as safe because the text is always 
# going to be provided by the editorial team.
# TODO: This would be dangerous if we ever had user-supplied text.
# We'd need to be more careful to escape HTML.
@register.filter
def smartlines(text):
	text = smartypants(text)
	text = text.replace("<br /><br />","</p><p>")
	return mark_safe(text)
