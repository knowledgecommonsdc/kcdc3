import unicodecsv, datetime
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from datetime import datetime
from django.views.generic import DetailView, TemplateView, ListView
from models import Event, Registration, Bio, Session, Location
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.template import Context
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from email import send_registration_mail
from helpers import *
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User	# for username export

# display a list of events
class EventListView(ListView):

	context_object_name = "event_list"
	model = Event

	def get_context_data(self, **kwargs):

		context = super(EventListView, self).get_context_data(**kwargs)

		context['events'] = Event.objects.filter(status='PUBLISHED', session__status="CURRENT")

		context['selected_session'] = Session.objects.filter(status="CURRENT")

		# get list of sessions for use in local navigation
		context['sessions'] = Session.objects.filter(Q(status='PAST')|Q(status='CURRENT'))

		return context



# display a list of archived (past or future) events
class EventArchiveView(ListView):

	template_name = "classes/event_archive.html"
	context_object_name = "event_list"
	model = Event

	def get_context_data(self, **kwargs):

		context = super(EventArchiveView, self).get_context_data(**kwargs)

		context['events'] = Event.objects.filter(status='PUBLISHED', session__slug=self.kwargs['slug'])
		context['selected_session'] = Session.objects.filter(slug=self.kwargs['slug'])


		# get list of sessions for use in local navigation
		context['sessions'] = Session.objects.filter(Q(status='PAST')|Q(status='CURRENT'))

		return context



# more about a particular session
class SessionView(ListView):

	template_name = "classes/event_session.html"
	context_object_name = "event_list"
	model = Event

	def get_context_data(self, **kwargs):

		context = super(SessionView, self).get_context_data(**kwargs)

		context['selected_session'] = Session.objects.filter(slug=self.kwargs['slug'])

		# get list of sessions for use in local navigation
		context['sessions'] = Session.objects.filter(Q(status='PAST')|Q(status='CURRENT'))

		return context



# display a single event
class EventDetailView(DetailView):

	context_object_name = "event"
	model = Event

	def get_context_data(self, **kwargs):

		context = super(EventDetailView, self).get_context_data(**kwargs)

		# get list of sessions for use in local navigation
		context['sessions'] = Session.objects.filter(Q(status='PAST')|Q(status='CURRENT'))

		if self.request.user.is_authenticated():
			context['user_is_authenticated'] = True
			user = self.request.user
		else:
			user = None

		event = self.get_object()

		context['registration_count'] = event.registration_count()
		context['waitlist_count'] = event.waitlist_count()
		context['user_is_waitlisted'] = is_waitlisted(user, event)
		context['user_is_registered'] = is_registered(user, event)
		context['is_registration_open'] = event.is_registration_open()
		context['add_to_waitlist'] = event.add_to_waitlist()

		# TODO: move this
		if self.request.user.is_authenticated():
			if Event.objects.filter(slug=self.object.slug, facilitators=self.request.user).count() > 0 or self.request.user.is_staff:
				context['show_facilitator'] = True

		if event.status == 'PUBLISHED' or event.status == 'HIDDEN':
			return context
		else:
			raise Http404



# handle registration/waitlist form
def register(request, slug):

	e = Event.objects.get(slug=slug)
	u = request.user

	# if there are no non-cancelled registrations for this user/event and
	# registration is possible
	if (is_registered(u, e) == False and
		is_waitlisted(u, e) == False and
		e.is_registration_open() == True):
		# Since the event object will become aware of this registration
		# as soon as it saves, we need to cache the value. This might bite us?
		#
		# Check it:
		#
		# There's a class with a size of one with waitlist enabled. If
		# we save now the check to send the email will happen after the
		# class number gets counted and the waitlist email will be sent.
		waitlist_status = e.add_to_waitlist()
		t = Registration(student=u,
			event=e,
			date_registered=datetime.now(),
			waitlist=waitlist_status)
		t.save()

		# Email us with the needs of the student.
		if request.POST["student_needs"] != "":
			send_mail("(KCDC accommodation form) " + e.title,
				request.user.email+" requested the following: "+request.POST["student_needs"],
				request.user.email,
				[settings.PROJECT_EMAIL],
				fail_silently=False)

		if waitlist_status == False:
			send_registration_mail(e, 'registered', request.user.email)
			return HttpResponseRedirect("/classes/response/registered")
		else:
			send_registration_mail(e, 'waitlisted', request.user.email)
			return HttpResponseRedirect("/classes/response/waitlisted")

	else:
		return HttpResponseRedirect("/classes/response/error")



# handle cancel form
def cancel(request, slug):

	e = Event.objects.get(slug=slug)

	if not is_cancelled(request.user, e) and (is_registered(request.user, e) or is_waitlisted(request.user, e)):
		# Gotta cache again... There's gotta be another way
		# to do this, this makes me feel gross.
		add_to_waitlist = e.add_to_waitlist()
		student_is_waitlisted = is_waitlisted(request.user, e)

		cancel_registration(request.user, e)
		if (add_to_waitlist == True and
			e.waitlist_status == True and
			not student_is_waitlisted and
			e.waitlist_count() > 0):
			student = promote_waitlistee(e)
			send_registration_mail(e, 'promoted', student.email)
		send_registration_mail(e, 'cancelled', request.user.email)
		return HttpResponseRedirect("/classes/response/cancelled")
	else:
		return HttpResponseRedirect("/classes/response/error")



# redirect the user to a thank you/results sceen after they take an action
class ResponseTemplateView(TemplateView):

	template_name = "classes/response.html"

	def get_context_data(self, **kwargs):
		if self.kwargs['slug'] == "registered":
			message_text = "registered"
		elif self.kwargs['slug'] == "waitlisted":
			message_text = "waitlisted"
		elif self.kwargs['slug'] == "cancelled":
			message_text = "cancelled"
		else:
			message_text = "Error"
		return {'message': message_text}



# teacher/facilitator view
@login_required
def facilitator(request, slug):

	e = Event.objects.get(slug=slug)

	context = Context()

	# get list of sessions for use in local navigation
	context['sessions'] = Session.objects.filter(Q(status='PAST')|Q(status='CURRENT'))

	context['slug'] = slug
	context['title'] = e.title
	context['teacher_bios'] = e.teacher_bios
	context['facilitators'] = e.facilitators.all

	context['registration_count'] = e.registration_count()
	context['waitlist_count'] = e.waitlist_count()

	context['registered_students'] = Registration.objects.filter(event=e, waitlist=False, cancelled=False)
	context['waitlisted_students'] = Registration.objects.filter(event=e, waitlist=True, cancelled=False)

	# is the user staff or assigned as a facilitator for this class?
	if Event.objects.filter(slug=slug, facilitators=request.user).count() > 0 or request.user.is_staff:
		return render_to_response('classes/facilitator_event_detail.html',context)
	else:
		# TODO this should really return a 403
		return HttpResponse()



# each student can see a list of courses for which they are registered
# eventually will expand into a list of courses for each student/teacher
# display a list of registrations for a given session
class UserEventListView(ListView):

	template_name = "classes/user_event_list.html"
	model = Registration

	def get_context_data(self, **kwargs):

		context = super(UserEventListView, self).get_context_data(**kwargs)

		context['registration_list'] = Registration.objects.filter(student=self.request.user).order_by('-event__date')

		return context

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(UserEventListView, self).dispatch(*args, **kwargs)




# staff dashboard
# display a list of registrations for a given session
class RegistrationListView(ListView):

	template_name = "classes/staff_registration_list.html"
	context_object_name = "registration_list"
	model = Registration

	@method_decorator(permission_required('classes.view_students', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(RegistrationListView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):

		context = super(RegistrationListView, self).get_context_data(**kwargs)
		context['events'] = Registration.objects.filter(event__session__slug=self.kwargs['slug'])
		return context




# staff dashboard
# display a list of sessions
class SessionAdminListView(ListView):

	template_name = "classes/staff_session_list.html"
	context_object_name = "session_list"
	model = Session

	@method_decorator(permission_required('classes.view_students', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(SessionAdminListView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):

		context = super(SessionAdminListView, self).get_context_data(**kwargs)
		context['session_list'] = Session.objects.all()
		return context




# staff dashboard
# display a list of teacher (bios) in the system
class TeacherAdminListView(ListView):

	template_name = "classes/staff_teacher_list.html"
	context_object_name = "teacher_list"
	model = Bio

	@method_decorator(permission_required('classes.view_students', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(TeacherAdminListView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):

		context = super(TeacherAdminListView, self).get_context_data(**kwargs)
		context['teacher_list'] = Bio.objects.all().order_by('name')
		return context



# staff dashboard
class FilteredTeacherAdminListView(TeacherAdminListView):

	@method_decorator(permission_required('classes.view_students', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(FilteredTeacherAdminListView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):

		context = super(TeacherAdminListView, self).get_context_data(**kwargs)
		context['teacher_list'] = Bio.objects.filter(event__session__slug__iexact=self.kwargs['slug']).order_by('name')
		return context

		# if self.kwargs['slug'] is not None:
		# 	context['teacher_list'] = Bio.objects.filter(name__contains="teacher")



# staff data access
# provide JSON of classes and registrations
# intended to back up attendance visualization
class JSONVizSessionAttendanceDataListView(ListView):

	template_name = "classes/data/session_attendance_list.json"
	context_object_name = "event_list"
	model = Event

	@method_decorator(permission_required('classes.view_students', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(JSONVizSessionAttendanceDataListView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):

		context = super(JSONVizSessionAttendanceDataListView, self).get_context_data(**kwargs)

		context['events'] = Event.objects.filter(status='PUBLISHED', session__slug=self.kwargs['slug'])

		return context


# staff data access
# provide CSV of classes and registrations
@permission_required('classes.view_students')
def csv_session_attendance_data(request, slug):

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="export.csv"'

	events = Event.objects.filter(status='PUBLISHED', session__slug=slug)

	writer = unicodecsv.writer(response)

	writer.writerow([
				'title',
				'date',
				'registered',
				'attended',
				'not attended',
				'waitlist',
				])

	for event in events:
		writer.writerow([
					event.title,
					event.date.strftime(settings.DATE_FORMAT_DATETIME_INTERCHANGE),
					event.registration_count(),
					event.attended_count(),
					event.registration_count() - event.attended_count(),
					event.waitlist_count(),
					])

	return response



# staff data access
# provide CSV of individual registrations
@permission_required('classes.view_students')
def csv_session_registration_data(request, slug):

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="export.csv"'

	registrations = Registration.objects.filter(event__session__slug__iexact=slug)

	writer = unicodecsv.writer(response)

	writer.writerow([
				'session',
				'event',
				'event date',
				'username',
				'date registered',
				'date canceled',
				'date promoted',
				'waitlist',
				'attended',
				'registered hours',
				'promoted hours',
				'canceled hours',
				'date user joined',
				])


	for registration in registrations:

		# Ensure we're passing empty strings instead of trying to format nulls

		if registration.date_cancelled is not None:
			date_cancelled = registration.date_cancelled.strftime(settings.DATE_FORMAT_DATETIME_INTERCHANGE)
		else:
			date_cancelled = ''

		if registration.date_promoted is not None:
			date_promoted = registration.date_promoted.strftime(settings.DATE_FORMAT_DATETIME_INTERCHANGE)
		else:
			date_promoted = ''

		writer.writerow([
					registration.event.session.slug,
					registration.event,
					registration.event.date.strftime(settings.DATE_FORMAT_DATETIME_INTERCHANGE),
					registration.student.username,
					registration.date_registered.strftime(settings.DATE_FORMAT_DATETIME_INTERCHANGE),
					date_cancelled,
					date_promoted,
					registration.waitlist,
					registration.attended,
					registration.get_registered_interval(),
					registration.get_promoted_interval(),
					registration.get_cancelled_interval(),
					registration.student.date_joined.strftime(settings.DATE_FORMAT_DATE_INTERCHANGE),
					])

	return response



# staff data access
# provide TXT of locations for a session
@permission_required('classes.view_students')
def txt_location_data(request):

	context = Context()
	context['locations'] = Location.objects.all()

	return render_to_response('classes/data/locations.txt', context, mimetype="text/plain")


# staff data access
# provide GeoJSON of locations for a session
def json_location_data(request):

	context = Context()

	# return only locations that have a specified lat/lng
	context['locations'] = Location.objects.filter(lat__isnull=False,lng__isnull=False)

	return render_to_response('classes/data/locations.json', context, mimetype="text/plain")


# staff/public data access
# provide JSON of classes and locations
def json_event_location_data(request):

	context = Context()

	# only returns locations that have a specified lat/lng
	context['events'] = Event.objects.filter(status = 'PUBLISHED', cancelled = False, location__lat__isnull=False, location__lng__isnull=False)

	return render_to_response('classes/data/event_locations.json', context, mimetype="text/plain")


# staff/public data access
# provide TSV of locations and classes in each location
def tsv_events_by_location_data(request):

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="export.csv"'

	events = Event.objects.filter(status = 'PUBLISHED', cancelled = False)

	writer = unicodecsv.writer(response)

	writer.writerow([
				'session',
				'class',
				'location',
				])


	for event in events:

		# Ensure we're passing empty strings instead of trying to format nulls

		if event.location:
			location_name = event.location
		else:
			location_name = ''

		writer.writerow([
					event.session.slug,
					event.title,
					event.location,
					])

	return response



# staff data access
# provide CSV of registered, active users
# Really doesn't belong here but this is a good spot
# until we integrate Tastypie
@permission_required('classes.view_students')
def csv_users_data(request):

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="export.csv"'

	active_users = User.objects.filter(is_active=True)

	writer = unicodecsv.writer(response)

	writer.writerow([
				'first_name',
				'last_name',
				'email',
				])

	for user in active_users:
		writer.writerow([
					user.first_name,
					user.last_name,
					user.email,
					])

	return response
