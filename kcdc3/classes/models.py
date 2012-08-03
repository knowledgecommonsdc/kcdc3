from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
	
	title = models.CharField(max_length=200)
	slug = models.SlugField(unique=True)
	STATUS_CHOICES = (
		('PUBLISHED', 'Published'),
		('HIDDEN', 'Hidden'),
		('DRAFT', 'Draft'),
		('REMOVED', 'Removed'),
	)
	status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='PUBLISHED')
	featured = models.BooleanField(default=False)
	
	date = models.DateTimeField('First meeting')
	additional_dates_text = models.TextField('Notes about additional meetings', blank=True)

	location_name = models.CharField(max_length=100, blank=True)
	location_address1 = models.CharField('address', max_length=60, blank=True)
	location_address2 = models.CharField('line two', max_length=60, blank=True)
	location_city = models.CharField('city', max_length=60, blank=True, default='Washington')
	location_state = models.CharField('state', max_length=2, blank=True, default='DC')
	location_zip = models.CharField('ZIP', max_length=5, blank=True)
	location_description = models.TextField('Location details', blank=True)
	location_show_exact = models.BooleanField('Show details/exact address on public site?', default=True)
	
	TYPE_CHOICES = (
		('CLASS', 'Class'),
		('EVENT', 'Event'),
		('EXTERNAL', 'Non-KCDC Event'),
	)
	type = models.CharField(max_length=9, choices=TYPE_CHOICES, default='CLASS')

	summary = models.TextField(blank=True)
	description = models.TextField(blank=True)
	thumbnail = models.ImageField(upload_to='event_images', blank=True, null=True)
	main_image = models.ImageField(upload_to='event_images', blank=True, null=True)

	email_welcome_text = models.TextField('Additional welcome email text', blank=True)
	email_reminder = models.BooleanField('Send reminder email?', default=True)
	email_reminder_text = models.TextField('Additional reminder email text', blank=True)

	documentation = models.TextField(blank=True)
	
	max_students = models.IntegerField('Max students', blank=True, null=True)
	waitlist_status = models.BooleanField('Use waitlist', default=True)
	
	REGISTRATION_STATUS_CHOICES = (
		('AUTO', 'Follow session settings'),
		('ALLOW', 'Allow registration'),
		('PREVENT', 'Prevent registration'),
		('HIDE', 'Hide registration forms'),
	)
	registration_status = models.CharField(max_length=7, choices=REGISTRATION_STATUS_CHOICES, default='AUTO')

	teachers = models.ManyToManyField(User, blank=True, null=True, related_name='teachers')
	facilitators = models.ManyToManyField(User, blank=True, null=True, related_name='facilitators')
	students = models.ManyToManyField(User, through='Registration', blank=True, null=True, related_name='students')
		
	class Meta:
		ordering = ['date']
	def __unicode__(self):
		return self.title
	def registration_count(self):
		return Registration.objects.filter(event__slug=self.slug,waitlist=False,cancelled=False).count()
	def waitlist_count(self):
		return Registration.objects.filter(event__slug=self.slug,waitlist=True,cancelled=False).count()
	def add_to_waitlist(self):
		if Registration.objects.filter(event__slug=self.slug,waitlist=False,cancelled=False).count() >= self.max_students and self.waitlist_status:
			return True
		else:
			return False
		
class Registration(models.Model):
	student = models.ForeignKey(User, null=True)
	event = models.ForeignKey(Event, null=True)
	date_registered = models.DateTimeField(auto_now_add=True)
	waitlist = models.BooleanField()
	attended = models.NullBooleanField()
	cancelled = models.BooleanField(default=False)
	date_cancelled = models.DateTimeField(blank=True, null=True)
	class Meta:
		ordering = ['date_registered']
