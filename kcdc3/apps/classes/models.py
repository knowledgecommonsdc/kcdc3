from django.db import models
from django.contrib.auth.models import User
import datetime
from datetime import timedelta
from format_helpers import *

# TODO this shouldn't be here but don't have settings import working yet
# In hours, how long before a class do late promotion rules apply?
WAITLIST_LATE_PROMOTION_TIME = 24


# a Session is a collection of classes
class Session(models.Model):
	title = models.CharField(max_length=200)
	long_title = models.CharField(max_length=200)
	slug = models.SlugField(unique=True)
	STATUS_CHOICES = (
		('CURRENT', 'Current'),
		('PAST', 'Past'),
		('HIDDEN', 'Hidden'),
	)
	status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='CURRENT')

	kicker = models.CharField('Kicker (for Classes page hed)', max_length=200, blank=True)
	description = models.TextField('Intro/Description', blank=True)
	sidebar_text = models.TextField('Sidebar', blank=True)
	show_sidebar_text = models.BooleanField(default=True)
	documentation = models.TextField('Documentation/Extended Text', blank=True)

	REGISTRATION_STATUS_CHOICES = (
		('ALLOW', 'Allow'),
		('PREVENT', 'Prevent'),
	)
	registration_status = models.CharField(max_length=7, choices=REGISTRATION_STATUS_CHOICES, default='PREVENT')
	email_reminder_days = models.IntegerField('Send reminder emails this many days ahead of classes:', default=2)

	class Meta:
		ordering = ['slug']

	def __unicode__(self):
		return self.title

	# Report regular, published classes
	def get_live_classes(self):
		return Event.objects.filter(session=self,status="PUBLISHED",type="CLASS")

	# Report regular, published classes
	def get_registrations(self):
		return Registration.objects.filter(event__session=self,cancelled=False,waitlist=False)

	# Report regular, published classes
	def get_attended_registrations(self):
		return Registration.objects.filter(event__session=self,cancelled=False,attended=True)




class Location(models.Model):
	name = models.CharField('Description', max_length=100, blank=True)
	neighborhood = models.CharField('Neighborhood', max_length=100, blank=True)
	address1 = models.CharField('Address', max_length=60, blank=True)
	address2 = models.CharField('Line two', max_length=60, blank=True)
	city = models.CharField('City', max_length=60, blank=True, default='Washington')
	state = models.CharField('State', max_length=2, blank=True, default='DC')
	zip = models.CharField('ZIP', max_length=5, blank=True)
	hint = models.CharField('Hint', max_length=300, blank=True)
	show_exact = models.BooleanField('Show details/exact address on public site?', default=True)
	LOCATION_ACCESS_CHOICES = (
		('public', 'Public'),
		('semipublic', 'Semi-Public'),
		('private', 'Private'),
	)
	access = models.CharField(max_length=11, choices=LOCATION_ACCESS_CHOICES, default='SEMIPUBLIC')
	lat = models.FloatField('Latitude',blank=True,null=True)
	lng = models.FloatField('Longitude',blank=True,null=True)
	def __unicode__(self):
		return self.name


# Organizations with whom KCDC is working
class Partner(models.Model):
	name = models.CharField('Name', max_length=100, blank=False, unique=True)
	description = models.TextField('Description', blank=True)
	website = models.URLField(blank=True)
	image = models.ImageField('Image (150x150px max)', upload_to='partners', blank=True, null=True)

	class Meta:
		verbose_name=u'Location Partner'

	def __unicode__(self):
		return self.name



# A group that a person is part of
class Role(models.Model):
	
	name = models.CharField('Name', max_length=48)
	description = models.TextField(blank=True)
	extended_description = models.TextField(blank=True)
	sort_order = models.IntegerField(blank=True, null=True, default=50)

	class Meta:
		ordering = ['sort_order']
		verbose_name=u'Staff Team/Group'
		verbose_name_plural=u'Staff Teams/Groups'

	def __unicode__(self):
		return self.name

	



class Bio(models.Model):

	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='user')

	# Basic information, used in class descriptions and elsewhere by default
	name = models.CharField('Name', max_length=100, blank=False, unique=True)
	description = models.TextField('Bio text', blank=True)
	web = models.CharField('Website', max_length=255, blank=True)
	image = models.ImageField('Image (160x160px)', upload_to='bio', blank=True, null=True)
	twitter = models.CharField('Twitter Handle', max_length=16, blank=True)
	show_email = models.BooleanField('Show email to public?', default=False)

	# No longer in use. Why? Because Django insists on adding a slash
	# to the end of URLFields, and defining my own field type seems excessive
	website = models.URLField(blank=True)

	# Fields for staff bios
	title = models.CharField(max_length=100, blank=True)
	staff_description = models.TextField('Staff bio text', blank=True)
	role = models.ForeignKey(Role, blank=True, null=True, on_delete=models.SET_NULL, related_name='role')

	# Fields for internal use
	rating = models.IntegerField('Rating', null=True, blank=True)
	comments = models.TextField('Comments', null=True, blank=True)
	bio_email = models.EmailField(null=True, blank=True)

	# Provide a filled-out description if one is available
	def get_staff_description(self):
		
		if self.staff_description:
			return self.staff_description
		else: 	
			return self.description

	# Provide Twitter handle with at-sign removed
	def get_twitter(self):
		tmp = self.twitter.replace("@","")
		return tmp

	# Provide website address; add http:// if no protocol is specified
	def get_web(self):
		return add_protocol(self.web)

	# Provide website with http:// removed
	def get_plain_web(self):
		return remove_protocol(self.web)

	# Provide email from bio; otherwise email from user
	def get_email(self):
		
		if self.bio_email:
			return self.bio_email
		elif self.user:
			return self.user.email
		else:
			return ""
	    		
	# Which classes is this person teaching?
	def get_classes(self):
		
		return Event.objects.filter(teacher_bios=self)
			
	class Meta:
		ordering = ['name']
		verbose_name=u'Teacher/Staff Bio'

	def __unicode__(self):
		return self.name



# an Event is a single class or other event
class Event(models.Model):
	
	# fundamentals
	title = models.CharField(max_length=200)
	slug = models.SlugField(unique=True)
	STATUS_CHOICES = (
		('PUBLISHED', 'Published'),
		('HIDDEN', 'Hidden'),
		('DRAFT', 'Draft'),
		('REMOVED', 'Removed'),
	)
	status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='PUBLISHED')
	
	# show on front page
	featured = models.BooleanField(default=False)
	
	# dates
	session = models.ForeignKey(Session, blank=False, null=True, on_delete=models.SET_NULL, related_name='session')
	date = models.DateTimeField('First meeting')
	end_time = models.TimeField('End time', blank=True, null=True)
	additional_dates_text = models.TextField('Notes about additional meetings', blank=True)

	# locational
	location = models.ForeignKey(Location, blank=True, null=True, on_delete=models.SET_NULL, related_name='location')
	partner = models.ForeignKey(Partner, blank=True, null=True, on_delete=models.SET_NULL, related_name='partner')
	
	#TODO: `type' keyword is reserved, and using it is considered naughty.
	TYPE_CHOICES = (
		('CLASS', 'Class'),
		('EVENT', 'Event'),
		('EXTERNAL', 'Non-KCDC Event'),
	)
	type = models.CharField(max_length=9, choices=TYPE_CHOICES, default='CLASS')

	# descriptive text
	summary = models.TextField('Teaser', blank=True)
	description = models.TextField(blank=True)
	details = models.TextField('Pre-class details', blank=True)
	documentation = models.TextField(blank=True)
	
	# list view
	TN_SMALL = 'small'
	TN_LARGE = 'large'
	LIST_LAYOUT_CHOICES = (
		(TN_SMALL, 'Small'),
		(TN_LARGE, 'Large'),
	)
	list_layout = models.CharField(max_length=5, choices=LIST_LAYOUT_CHOICES, default=TN_LARGE)
	thumbnail = models.ImageField('Thumbnail (max 432px wide)', upload_to='event_images', blank=True, null=True)

	# detail view
	IMG_SMALL = 'small'
	IMG_LARGE = 'large'
	IMG_LAYOUT_CHOICES = (
		(IMG_SMALL, 'Small'),
		(IMG_LARGE, 'Large'),
	)
	img_layout = models.CharField(max_length=5, choices=IMG_LAYOUT_CHOICES, default=IMG_LARGE)
	main_image = models.ImageField('Main image (max 660px wide)', upload_to='event_images', blank=True, null=True)
	caption = models.TextField(blank=True)

	# email reminders
	email_welcome_text = models.TextField('Extra text for welcome email', blank=True)  
	email_reminder = models.BooleanField('Send reminder email?', default=True)  # unused
	email_reminder_text = models.TextField('Extra text for reminder email', blank=True)  # unused

	# student numbers and waitlist
	max_students = models.IntegerField('Max students', blank=True, null=True, default=999)
	waitlist_status = models.BooleanField('Use waitlist', default=True)
	
	# registration control
	REGISTRATION_STATUS_CHOICES = (
		('AUTO', 'Auto'),
		('ALLOW', 'Allow (+)'),
		('PREVENT', 'Prevent (-)'),
		('HIDE', 'Hide forms'),
	)
	registration_status = models.CharField(max_length=7, choices=REGISTRATION_STATUS_CHOICES, default='AUTO')
	registration_opens = models.DateTimeField(blank=True, null=True)

	# people associated with this class
	teacher_bios = models.ManyToManyField(Bio, blank=True, null=True, related_name='event')
	teachers = models.ManyToManyField(User, blank=True, null=True, related_name='teachers')
	facilitators = models.ManyToManyField(User, blank=True, null=True, related_name='facilitators')
	students = models.ManyToManyField(User, through='Registration', blank=True, null=True, related_name='students')

	# optional, course-by-course bio text
	bio_text = models.TextField('Alternative teacher bio text for this class',blank=True)	

	# legacy fields
	teacher_text = models.CharField('Teacher (text)', max_length=200, blank=True)
	location_text = models.CharField('Location (text)', max_length=300, blank=True)
		
	class Meta:
		ordering = ['-date']
		verbose_name=u'Class/Event'
		verbose_name_plural=u'Classes/Events'

	def __unicode__(self):
		return self.title

	def has_passed(self):
		""" Determines if the class date is before now."""
		return self.date < datetime.datetime.now()

	def get_registrations(self, waitlist=False, cancelled=False):
		""" Returns all the registrations associated with this event."""
		return Registration.objects.filter(
			event__slug=self.slug,
			waitlist=waitlist,
			cancelled=cancelled)

	def registration_count(self):
		""" Determines the total number of registrations for a class.
		This does not include the waitlist."""
		return self.get_registrations().count()

	def waitlist_count(self):
		""" Determines the total number of waitlisted registrations."""
		return self.get_registrations(waitlist=True).count()

	def add_to_waitlist(self):
		""" Checks to see if the class is full and has a waitlist.
		If it is full and has a waitlist it returns true, false 
		otherwise."""
		if self.get_registrations().count() >= self.max_students and self.waitlist_status:
			return True
		else:
			return False

	def num_teachers(self):
		""" Returns the number of bios associated with this event."""
		return self.teacher_bios.count()

	def is_registration_open(self):
		""" Returns whether a user can register for the class or not."""
		if self.date < datetime.datetime.now():
			return False
		elif self.registration_status == 'ALLOW':
			return True
		elif self.registration_status == 'AUTO' and self.registration_opens:
			if self.registration_opens < datetime.datetime.now():
				return True
			else: 
				return False
		else: 
			return False
			
	def is_late_promotion(self):
		""" True if a user is being promoted from the waitlist 
		close to the class meeting time."""
		if (self.date <= datetime.datetime.now() + timedelta(hours=WAITLIST_LATE_PROMOTION_TIME)):
			return True
		else:
			return False
		

# Registrations connect Users with the Events they've signed up for		
class Registration(models.Model):
	student = models.ForeignKey(User, null=True)
	event = models.ForeignKey(Event, null=True)
	date_registered = models.DateTimeField(auto_now_add=True)
	waitlist = models.BooleanField()
	attended = models.NullBooleanField()
	cancelled = models.BooleanField(default=False)
	date_cancelled = models.DateTimeField(blank=True, null=True)
	date_promoted = models.DateTimeField(blank=True, null=True)
	late_promotion = models.BooleanField(default=False)

	class Meta:

		ordering = ['date_registered']

		#TODO this isn't being picked up by the admin
		permissions = (
			("view_students", "Can see enrolled students"),
			("record_attendance", "Can mark student attendance"),
			("edit_students", "Can add or remove students"),
		)


