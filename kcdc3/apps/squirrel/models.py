from django.db import models
from django.contrib.auth.models import User
import datetime
from datetime import timedelta
# from format_helpers import *
from kcdc3.apps.classes.models import Location

"""

Squirrel provides admin services for staff.
The major feature is meeting RSVPs.

The code overlap with Classes suggests the use of base classes, 
but keeping the two apps separate affords a chance to experiment, 
at least for the moment. Classes is getting rambly. Squirrel can
diverge and take a more minimalist approach.

"""




"""
An Meeting is a meeting for staff.
This object shares characteristics with the Event obj in Classes. 
"""
class Meeting(models.Model):
	
	title = models.CharField(max_length=200)
	slug = models.SlugField(unique=True)
	STATUS_CHOICES = (
		('PUBLISHED', 'Published'),
		('HIDDEN', 'Hidden'),
		('DRAFT', 'Draft'),
		('REMOVED', 'Removed'),
	)
	status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='PUBLISHED')

	date = models.DateTimeField('First meeting')
	end_time = models.TimeField('End time', blank=True, null=True)
	location = models.ForeignKey(Location, blank=True, null=True, on_delete=models.SET_NULL, related_name='squirrel_location')
	
	description = models.TextField(blank=True)
		
	class Meta:
		ordering = ['-date']

	def __unicode__(self):
		return self.title

	def has_passed(self):
		""" Determines if the class date is before now."""
		return self.date < datetime.datetime.now()

	def get_registrations(self, cancelled=False):
		""" Returns all the registrations associated with this event."""
		return Meeting_Registration.objects.filter(
			meeting__slug=self.slug,
			cancelled=cancelled)

	def registration_count(self):
		""" Determines the total number of registrations for a class.
		This does not include the waitlist."""
		return self.get_registrations().count()

		

# Meeting_Registrations connect Users with the Meetings they've signed up for		
class Meeting_Registration(models.Model):
	user = models.ForeignKey(User, null=True, related_name='squirrel_user')
	meeting = models.ForeignKey(Meeting, null=True)
	date_registered = models.DateTimeField(auto_now_add=True)
	cancelled = models.BooleanField(default=False)
	note = models.TextField(blank=True)

	class Meta:
		ordering = ['date_registered']
		verbose_name=u'Meeting Registration'
