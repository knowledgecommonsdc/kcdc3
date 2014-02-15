"""This module provides a bunch of helper functions to deal with user
registration stuff."""

from models import Meeting, Meeting_Registration
from django.contrib.auth.models import User
from datetime import datetime, timedelta



def is_registered(user, meeting):
	"""Checks to see if a user is registered for a given meeting."""
	if user == None:
		return False

	user_registrations = Meeting_Registration.objects.filter(
					meeting=meeting, 
					user=user
					)	
	if len(user_registrations) > 0:
		return True
	else:
		return False



def get_user_rsvp(user, meeting):
	"""Returns a user's RSVP for a given meeting."""
	if user == None:
		return ''

	user_registrations = Meeting_Registration.objects.filter(
					meeting=meeting, 
					user=user
					)	
	if len(user_registrations) > 0:
		return user_registrations[0].status
	else:
		return ''


