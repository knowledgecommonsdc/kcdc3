"""This module provides an interface to send email easily. There's 
a lot of copy paste code for email, this'll be my attempt to rectify
that situation.
"""

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from models import Event

KCDC_EMAIL = 'contact@knowledgecommonsdc.org'

SUBJECT_REGISTERED = 'classes/email_registered_subject.txt'
SUBJECT_WAITLISTED = 'classes/email_waitlisted_subject.txt'
SUBJECT_CANCELLED = 'classes/email_cancelled_subject.txt'
SUBJECT_PROMOTED = 'classes/email_promoted_subject.txt'

BODY_REGISTERED = 'classes/email_registered.txt'
BODY_WAITLISTED = 'classes/email_waitlisted.txt'
BODY_CANCELLED = 'classes/email_cancelled.txt'
BODY_PROMOTED = 'classes/email_promoted.txt'

class RegistrationEmail(EmailMessage):
	""" Wrapper class for the builtin EmailMessage class provided
	by django."""

	def __init__(self, event, registration_flag, **kwargs):
		super(EmailMessage,self).__init__()

		self.event = self.generate_context(event)

		self.subject = self.generate_subject(registration_flag)

		self.body = self.generate_message(registration_flag)

		self.from_email = kwargs.get('from_email', KCDC_EMAIL)

		self.to = [kwargs.get('to')]

		self.bcc = kwargs.get('bcc', [])

		""" Messages were getting CCed even when no CC recipient was specified. 
			Disabled for now, since we're not using this function anyway."""
		cc = kwargs.get('cc')
		self.cc = ['kcdc.waitlist@gmail.com']

		# cc = kwargs.get('cc')
		# if cc and cc != KCDC_EMAIL:
		# 	self.cc = [cc, KCDC_EMAIL]
		# else:
		# 	self.cc = [KCDC_EMAIL]

		self.connection = kwargs.get('connection')

		self.attachments = kwargs.get('attachments')

		self.headers = kwargs.get('headers')

		self.extra_headers = kwargs.get('extra_headers')
		self.extra_headers = {'From': self.from_email}

	def generate_context(self, event):
		"""Generate the set of key value pairs that will be used
		for all template population for the emails."""
		#TODO: I still think there has to be a better way to do
		# this sort of thing...
		return {
			'title': event.title,
			'slug': event.slug,
			'date': event.date,
			'end_time': event.end_time,
			'additional_dates_text': event.additional_dates_text,
			'location_name': event.location.name,
			'location_address1': event.location.address1,
			'location_address2': event.location.address2,
			'location_city': event.location.city,
			'location_state': event.location.state,
			'location_zip': event.location.zip,
			'location_neighborhood': event.location.neighborhood,
			'location_hint': event.location.hint,
			'details': event.details,
			'email_welcome_text': event.email_welcome_text,	
			'is_late_promotion': event.is_late_promotion,	
			}

	def generate_subject(self, registration_flag):
		"""Generate the subject line for the email that will be sent
		to the user regarding their registration status."""
		#TODO: This case statement is silly.
		if registration_flag == 'registered':
			return render_to_string(SUBJECT_REGISTERED, self.event)
		elif registration_flag == 'waitlisted':
			return render_to_string(SUBJECT_WAITLISTED, self.event)
		elif registration_flag == 'cancelled':
			return render_to_string(SUBJECT_CANCELLED, self.event)
		elif registration_flag == 'promoted':
			return render_to_string(SUBJECT_PROMOTED, self.event)
		else:
			raise ValueError("%s bad registration_flag" % 
				registration_flag)

	def generate_message(self, registration_flag):
		"""Generate either a email to alert the user that they have
		been registered for the class or that they've cancelled their
		registration."""
		#TODO: This case statement is also silly.
		if registration_flag == 'registered':
			return render_to_string(BODY_REGISTERED, self.event)
		elif registration_flag == 'waitlisted':
			return render_to_string(BODY_WAITLISTED, self.event)
		elif registration_flag == 'cancelled':
			return render_to_string(BODY_CANCELLED, self.event)
		elif registration_flag == 'promoted':
			return render_to_string(BODY_PROMOTED, self.event)
		else:
			raise ValueError("%s bad registration_flag" % 
				registration_flag)

def send_registration_mail(event, registration_flag, student):
	"""Helper function to facilitate the sending of email. Keeps things
	DRY."""
	email = RegistrationEmail(event, registration_flag, to=student)
	email.send()
