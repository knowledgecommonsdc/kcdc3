from models import Post
from kcdc3.apps.classes.models import Bio
from django import forms
from django.contrib import admin
from django.contrib.admin.sites import site
from django.contrib.admin.widgets import ManyToManyRawIdWidget
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_unicode
from django.utils.html import escape



class PostAdmin(admin.ModelAdmin):
	
	fieldsets = [
		(None, {'fields': [
			'title', 'slug', 'department_label', ('date', 'author', 'special_author',), ('status', 'featured',),
			]}),
		('Text', {
			'classes': ('grp-collapse grp-open',),
			'fields': [
			'thumbnail',
			'teaser',
			'main_text',
			]}),
		('Tags and comments', {
			'classes': ('grp-collapse grp-open',),
			'fields': [
			'tags',
			'allow_comments',
			]}),
	]

	prepopulated_fields = {"slug": ("title",)}
	raw_id_fields = ['author']
	related_lookup_fields = {
	    'm2m': ['author'],
	}

	list_display = ('title', 'date', 'status', 'featured', 'allow_comments', 'tags',)
	list_editable = ('status', 'featured',)

	class Media:
		js = [
			'tiny_mce/tiny_mce.js',
			'tiny_mce/tinymce_setup.js',
		]

admin.site.register(Post, PostAdmin)

