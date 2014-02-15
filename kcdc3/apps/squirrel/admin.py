from models import Meeting, Meeting_Registration
from kcdc3.apps.classes.models import Bio
from django import forms
from django.contrib import admin
from django.contrib.admin.sites import site
from django.contrib.admin.widgets import ManyToManyRawIdWidget
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_unicode
from django.utils.html import escape






# displays registrations as a list in the Event Admin screen
class RegistrationInline(admin.TabularInline):
	model = Meeting_Registration
	extra = 0
	classes = ('grp-collapse grp-closed',)
	# inline_classes = ('grp-collapse grp-open',)
	fields = ('user', 'date_registered', 'cancelled',)
	can_delete = False
	readonly_fields = ('date_registered',)
	raw_id_fields = ['user']
	related_lookup_fields = {
	    'fk': ['user'],
	}





# lets someone create/edit a Meeting
class MeetingAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,			{'fields': ['title', 'slug',('date','end_time'),('location'),('status')]}),
		('Description', {
			'classes': ('grp-collapse grp-open',), 
			'fields': [
				'description', 
			]
		}),
	]
	prepopulated_fields = {"slug": ("title",)}
	raw_id_fields = ['location']
	inlines = (RegistrationInline,)
	class Media:
		js = [
			'tiny_mce/tiny_mce.js',
			'tinymce_setup.js',
		]

	list_display = ('title', 'date',)
	search_fields = ('title',)

admin.site.register(Meeting, MeetingAdmin)
