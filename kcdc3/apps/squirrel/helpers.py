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
					user=user, 
					cancelled=False)	
	if len(user_registrations) > 0:
		return True
	else:
		return False

def is_cancelled(user, meeting):
	"""Checks to see if a user has cancelled for a given meeting."""
	if user == None:
		return False

	user_registrations = Meeting_Registration.objects.filter(
					meeting=meeting,
					user=user,
					cancelled=False)

	if len(user_registrations) > 0:
		return False
	else:
		return True


def cancel_registration(user, meeting):
	"""Cancels the users registration for an meeting."""
	registration = Meeting_Registration.objects.filter(
				meeting=meeting, 
				user=user, 
				cancelled=False)[0]
	registration.date_cancelled=datetime.now()
	registration.cancelled=True
	registration.save()

