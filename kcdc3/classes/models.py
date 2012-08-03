from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
	
	title = models.CharField(max_length=200)
	date = models.DateTimeField('First meeting')
	slug = models.SlugField(unique=True)
	summary = models.TextField(blank=True)
	description = models.TextField(blank=True)
	location_description = models.TextField(max_length=200, blank=True)
	
	max_students = models.IntegerField('Max size', blank=True, null=True)
	waitlist_status = models.BooleanField('Waitlist', default=True)
	
	REGISTRATION_STATUS_CHOICES = (
		('AUTO', 'Follow session settings'),
		('ALLOW', 'Allow registration'),
		('PREVENT', 'Prevent registration'),
		('HIDE', 'Hide registration forms'),
	)
	registration_status = models.CharField(max_length=7, choices=REGISTRATION_STATUS_CHOICES, default='AUTO')

	teachers = models.ManyToManyField(User, blank=True, null=True, related_name='teachers')
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
