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
		(None,			{'fields': ['title', 'date','slug']}),
		('Pre-Class Information', {
			'classes': ('grp-collapse grp-closed',), 
			'fields': ['summary', 'description', 'location_description']
		}),
		('Documentation', {
			'classes': ('grp-collapse grp-closed',), 
			'fields': []
		}),
		('Teachers/facilitators',	{'fields': ['teachers']}),
		('Size and waitlist',	{'fields': [('max_students', 'waitlist_status')]}),
	]
	raw_id_fields = ['teachers',]
	related_lookup_fields = {
	    'm2m': ['teachers'],
	}
	inlines = (RegistrationInline,)
	list_display = ('title', 'date','max_students', 'waitlist_status')
	prepopulated_fields = {"slug": ("title",)}

admin.site.register(Event, EventAdmin)
