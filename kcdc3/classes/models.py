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
	teachers = models.ManyToManyField(User, blank=True, null=True, related_name='teachers')
	students = models.ManyToManyField(User, through='Registration', blank=True, null=True, related_name='students')
	class Meta:
		ordering = ['date']
	def __unicode__(self):
		return self.title
		
class Registration(models.Model):
	student = models.ForeignKey(User, null=True)
	event = models.ForeignKey(Event, null=True)
	date_registered = models.DateTimeField()
	waitlist = models.BooleanField()
	attended = models.NullBooleanField()
	cancelled = models.BooleanField(default=False)
	date_cancelled = models.DateTimeField(blank=True, null=True)


