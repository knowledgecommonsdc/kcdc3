from kcdc3.apps.classes.models import Event, Location, Bio, Registration, Session, Role, Partner
from django import forms
from django.contrib import admin
from django.contrib.admin.sites import site
from django.contrib.admin.widgets import ManyToManyRawIdWidget, ForeignKeyRawIdWidget
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_unicode
from django.utils.html import escape
from django.contrib.auth.models import User



# displays registrations as a list in the Event Admin screen
class RegistrationInline(admin.TabularInline):
	model = Registration
	extra = 0
	classes = ('grp-collapse grp-closed',)
	# inline_classes = ('grp-collapse grp-open',)
	fields = ('student', 'date_registered', 'waitlist', 'cancelled', 'date_cancelled', 'attended', 'late_promotion', 'date_promoted')
	can_delete = False
	readonly_fields = ('date_registered','date_cancelled', 'late_promotion', 'date_promoted')
	raw_id_fields = ['student']
	related_lookup_fields = {
	    'fk': ['student'],
	}



class LocationAdmin(admin.ModelAdmin):
	model = Location
	list_display = ('name','neighborhood','show_exact','address1','lat','lng')
	list_filter = ('neighborhood',)
	list_editable = ('lat', 'lng')
	search_fields = ('name',)

admin.site.register(Location, LocationAdmin)



class RoleAdmin(admin.ModelAdmin):

	model = Role
	list_display = ('name', 'sort_order',)
	fieldsets = [
		(None, {'fields': ['name','description', 'extended_description', 'sort_order',]}),
	]

	class Media:
		js = [
			'tiny_mce/tiny_mce.js',
			'tinymce_setup.js',
		]

admin.site.register(Role, RoleAdmin)



class BioAdmin(admin.ModelAdmin):
	
	model = Bio
	list_display = ('name', 'user', 'role', 'title',)
	fieldsets = [
		(None, {'fields': ['name','user','image',]}),
		('Teacher bio', {
			'classes': ('grp-collapse grp-open',), 
			'fields': [
				'description', 'web', 'bio_email', 'show_email', 'twitter',
			]
		}),
		('Staff bio', {
			'classes': ('grp-collapse grp-open',), 
			'fields': [
				'role', 'title', 'staff_description', 
			],
		}),
		('Admin', {
			'classes': ('grp-collapse grp-open',), 
			'fields': [
				'rating', 'comments', 
			],
		}),
	]
	raw_id_fields = ['user']
	related_lookup_fields = {
	    'fk': ['user'],
	}

	list_filter = ('role',)
	search_fields = ('name',)

	class Media:
		js = [
			'tiny_mce/tiny_mce.js',
			'tinymce_setup.js',
		]

admin.site.register(Bio, BioAdmin)



# lets someone create/edit a Event
class EventAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,			{'fields': ['title', 'slug',('date','end_time','session'),('location','partner',),('status', 'featured','type',)]}),
		('Teachers/facilitators',	{'fields': [('teacher_bios','facilitators')]}),
		('Description', {
			'classes': ('grp-collapse grp-open',), 
			'fields': [
				'summary', 'description', ('thumbnail', 'main_image'), 
			]
		}),
		('Registration',	{'fields': [('registration_status', 'registration_opens',), ('max_students', 'waitlist_status', 'registration_count','waitlist_count'),]}),
		('More details', {
			'classes': ('grp-collapse grp-closed',), 
			'fields': [
				'details',
				'additional_dates_text',
				'bio_text',
			]
		}),
		('Automatic email messages', {
			'classes': ('grp-collapse grp-open',), 
			'fields': ['email_welcome_text',]
		}),
		('Documentation', {
			'classes': ('grp-collapse grp-closed',), 
			'fields': ['documentation']
		}),
		('Legacy data', {
			'classes': ('grp-collapse grp-closed',), 
			'fields': ['teacher_text','location_text']
		}),
	]
	readonly_fields = ('registration_count','waitlist_count')
	prepopulated_fields = {"slug": ("title",)}
	raw_id_fields = ['location','partner','teacher_bios','facilitators']
	related_lookup_fields = {
	    'm2m': ['teacher_bios', 'facilitators'],
	}
	inlines = (RegistrationInline,)
	class Media:
		js = [
			'tiny_mce/tiny_mce.js',
			'tinymce_setup.js',
		]

	list_display = ('title', 'status','date','session', 'featured', 'registration_status', 'registration_opens', 'waitlist_status','max_students', 'registration_count', 'waitlist_count',)
	list_editable = ('registration_status', 'featured', 'registration_opens',)
	list_filter = ('session', 'status', 'registration_status','type',)
	search_fields = ('title',)

admin.site.register(Event, EventAdmin)



# create/edit a Session
class SessionAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': [
			'title', 'long_title', 'slug', 'status',
			]}),
		# ('Registration', {
		# 	'classes': ('grp-collapse grp-closed',),
		# 	'fields': [
		# 	('registration_status', 
		# 	'email_reminder_days')
		# 	]}),
		('Text', {
			'classes': ('grp-collapse grp-open',),
			'fields': [
			'kicker',
			'description',
			'sidebar_text',
			'show_sidebar_text',
			]}),
		('Extended Text', {
			'classes': ('grp-collapse grp-open',),
			'fields': [
			'documentation',
			]}),
	]
	list_display = ('title', 'slug', 'status')
	class Media:
		js = [
			'tiny_mce/tiny_mce.js',
			'tinymce_setup.js',
		]

admin.site.register(Session, SessionAdmin)



class PartnerAdmin(admin.ModelAdmin):
	model = Partner
	list_display = ('name',)
	fieldsets = [
		(None, {'fields': ['name','description', 'website', 'image',]}),
	]
	class Media:
		js = [
			'tiny_mce/tiny_mce.js',
			'tinymce_setup.js',
		]

admin.site.register(Partner, PartnerAdmin)





# view all registrations
class RegistrationAdmin(admin.ModelAdmin):
	can_delete = False
	readonly_fields = ('student', 'event', 'date_registered', 'date_cancelled', 'late_promotion', 'date_promoted')
	raw_id_fields = ['student']
	fieldsets = [
		(None, {'fields': [
			'student', 'event', 'date_registered', 'waitlist', 'cancelled', 'date_cancelled', 'late_promotion', 'date_promoted', 'attended',  
			]}),
	]
	list_display = ('student', 'event', 'date_registered', 'waitlist', 'cancelled', 'late_promotion', 'attended', 'date_cancelled', 'date_promoted', )
	list_filter = ('date_registered', 'waitlist', 'cancelled', 'attended','late_promotion',)
	search_fields = ( 'student__username', 'student__email', )

admin.site.register(Registration, RegistrationAdmin)
