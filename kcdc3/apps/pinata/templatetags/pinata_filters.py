from django import template
from smartypants import smartypants
from django.utils.safestring import mark_safe
from django.conf import settings
from markdown_deux import markdown as markdown_deux

register = template.Library()


@register.filter
def smartquotes(text):
    return smartypants(text)

# Clean up text to match house style
#
# We are marking the results as safe because the text is always
# going to be provided by the editorial team. This would be dangerous
# if we ever had user-supplied text. We'd need to be more careful
# to escape HTML.
@register.filter
def smartlines(text):
	text = smartypants(text)
	text = text.replace("<br /><br />","</p><p>")
	return mark_safe(text)

# Process Markdown and clean up text to match house style
# For editorial text only, since text is marked safe.
#
# We are processing Markdown using Markdown Deux
# Config sets are in settings/common.py
@register.filter
def smartdown(text):
	text = smartypants(text)
	text = text.replace("<br /><br />","</p><p>")
	text = markdown_deux(text,"default")
	return mark_safe(text)

# Retrieve short phrases that are reused throughout the project
# Right now, these phrases are stored in settings.py
# Takes, as an argument, a string that identifies the phrase we want
def boilerplate(slug):

	if slug == 'project_name':
		return settings.PROJECT_NAME
	elif slug == 'project_short_name':
		return settings.PROJECT_SHORT_NAME
	elif slug == 'project_email':
		return settings.PROJECT_EMAIL
	elif slug == 'project_url':
		return settings.PROJECT_URL
	else:
		return ''

register.simple_tag(boilerplate)
