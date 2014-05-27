from datetime import date, timedelta

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMessage
from django.db.models import Q
from django.conf import settings

from kcdc3.apps.classes.models import Event
from kcdc3.apps.classes.email import send_reminder_email, send_reminder_qc_email

# TODO: use Event's email_welcome_text, email_reminder, email_reminder_text
# TODO: move all logic into separate class

class Command(BaseCommand):
	args = '<days_ahead>'
	help = 'Sends out email alerts to participants of all events that will occur <days_ahead> days from today (midnight to 11.59pm of that day, regardless of the current time today)'

	def handle(self, *args, **options):
		if len(args) != 1:
			raise CommandError('Please specify the number of days from today that you want to send reminders for.')
		alert_day = date.today() + timedelta(days=int(args[0]))
		print '{0}: Finding events for {1}...'.format(date.today(), alert_day)
		events = Event.objects.filter(
				Q(status='PUBLISHED') | Q(status='HIDDEN'),
				cancelled=False,
				date__year=alert_day.year, date__month=alert_day.month, date__day=alert_day.day
			)
		for event in events:
			self.send_emails_for_event(event)					 
		print 'Success!'

	def send_emails_for_event(self, event): 
		
		regs = event.get_registrations()
		print 'Sending emails for {0} ({1} students)...'.format(event.title, len(regs))
		for reg in regs:
			send_reminder_email(reg)
			
		# email the assigned facilitators
		for facilitator in event.facilitators.all():
			send_reminder_qc_email(event, facilitator.email)
			
		# also send a copy to the organization's main email address
		send_reminder_qc_email(event, settings.DEFAULT_FROM_EMAIL)

