from pinata.models import Page
from django import forms
from django.contrib import admin
from django.contrib.admin.sites import site
from django.contrib.admin.widgets import ManyToManyRawIdWidget, ForeignKeyRawIdWidget
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_unicode
from django.utils.html import escape



class PageAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': [
			'title', 'short_title', 'parent', 'path', 'status',
			]}),
		('Text', {
			'classes': ('grp-collapse grp-open',),
			'fields': [
			'teaser',
			'main_text'
			]}),
		('Additional Text', {
			'classes': ('grp-collapse grp-open',),
			'fields': [
			'sidebar_text',
			]}),
	]
	list_display = ('title', 'status', 'parent', 'path')
	class Media:
		js = [
			'tiny_mce/tiny_mce.js',
			'tinymce_setup.js',
		]

admin.site.register(Page, PageAdmin)

