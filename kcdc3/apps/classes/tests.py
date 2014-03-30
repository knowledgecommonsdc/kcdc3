"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from datetime import date, datetime, timedelta

from django.contrib.auth.models import User
from django.core import mail
from django.core.management import call_command
from django.test import TestCase

from kcdc3.apps.classes.models import Event, Location, Registration, Session

class EventTestCase(TestCase):
    fixtures = ["test"]
    pass

class ReminderEmailCase(TestCase):
    event_day_delta = 2

    def setUp(self):
        today = date.today()

        session = Session.objects.create(
            title='Test Session Title', 
            long_title='Test Session Long Title', 
            slug='Test Session Slug',
            status='CURRENT',
            kicker='Test Session Kicker',
            description='Test Session Description',
            sidebar_text='Test Session Sidebar Text',
            show_sidebar_text=True,
            documentation='Test Session Documentation',
            registration_status='ALLOW',
            email_reminder_days=5)

        location = Location.objects.create(
            name='Test Location Name')

        event = Event.objects.create(
            title='Test Event Title',
            slug='Test Event Slug',
            status='PUBLISHED',
            featured=False,
            session=session,
            date=today + timedelta(days=self.event_day_delta),
            location=location,
            type='CLASS',
            email_reminder=True,
            waitlist_status=True,
            registration_status='AUTO')

        user = User.objects.create(
            username='testuser',
            email='test@test.com',
            password='pwhash',
            is_staff=False,
            is_active=True,
            is_superuser=False,
            last_login=datetime.today(),
            date_joined=datetime.today())

        reg = Registration.objects.create(
            student=user,
            event=event,
            waitlist=False,
            attended=False,
            cancelled=False,
            late_promotion=False)

    def test_vanilla_send(self):
        mail.send_mail('subj', 'msg here', 'from@blah.com', ['to@to.com'], fail_silently=False)
        self.assertEqual(len(mail.outbox), 1)

    def test_base_email(self):
        call_command('send_reminder_emails', str(self.event_day_delta))
        self.assertEqual(len(mail.outbox), 1)
