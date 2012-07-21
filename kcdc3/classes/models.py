from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
	title = models.CharField(max_length=200)
	date = models.DateTimeField('First meeting')
	summary = models.TextField(blank=True)
	description = models.TextField(blank=True)
	location_description = models.TextField(max_length=200, blank=True)
	max_students = models.IntegerField('Max size', blank=True, null=True)
	waitlist_status = models.BooleanField('Waitlist', default=True)
	teachers = models.ManyToManyField(User, blank=True, null=True)
	def __unicode__(self):
		return self.title
	class Meta:
		ordering = ['date']
		
class Registration(models.Model):
	date_registered = models.DateTimeField()
	
	