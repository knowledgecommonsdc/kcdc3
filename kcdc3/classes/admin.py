from classes.models import Event, Registration
from django import forms
from django.contrib import admin
from django.contrib.admin.sites import site
from django.contrib.admin.widgets import ManyToManyRawIdWidget, ForeignKeyRawIdWidget
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_unicode
from django.utils.html import escape
from django.contrib.auth.models import User



class RegistrationInline(admin.TabularInline):
	model = Registration
	extra = 0
	classes = ('grp-collapse grp-closed',)
	# inline_classes = ('grp-collapse grp-open',)
	fields = ('student', 'date_registered', 'waitlist', 'cancelled', 'attended')
	can_delete = False
	readonly_fields = ('date_registered',)

class EventAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,			{'fields': ['title', 'slug',('date','type'), ('status', 'featured',)]}),
		('Teachers/facilitators',	{'fields': [('teachers','facilitators')]}),
		('Description', {
			'classes': ('grp-collapse grp-open',), 
			'fields': [
				'summary', 'description', ('thumbnail', 'main_image'), 
			]
		}),
		('Location', {
			'classes': ('grp-collapse grp-open',), 
			'fields': [
				'location_name', 'location_neighborhood', 'location_show_exact', 'location_address1', 'location_address2', 'location_city', ('location_state', 'location_zip'), 
			]
		}),
		('More pre-class details and additional dates', {
			'classes': ('grp-collapse grp-closed',), 
			'fields': [
				'details',
				'additional_dates_text',
			]
		}),
		('Email reminders', {
			'classes': ('grp-collapse grp-closed',), 
			'fields': ['email_welcome_text','email_reminder_text', 'email_reminder', ]
		}),
		('Post-class documentation', {
			'classes': ('grp-collapse grp-closed',), 
			'fields': ['documentation']
		}),
		('Registration',	{'fields': [('max_students', 'registration_status', 'waitlist_status','registration_count','waitlist_count')]}),
	]
	readonly_fields = ('registration_count','waitlist_count')
	raw_id_fields = ['teachers','facilitators']
	related_lookup_fields = {
	    'm2m': ['teachers', 'facilitators'],
	}
	inlines = (RegistrationInline,)
	list_display = ('title', 'date','max_students', 'registration_status', 'waitlist_status','registration_count','waitlist_count')
	prepopulated_fields = {"slug": ("title",)}
	class Media:
		js = [
			'tiny_mce/tiny_mce.js',
			'tinymce_setup.js',
		]

admin.site.register(Event, EventAdmin)
