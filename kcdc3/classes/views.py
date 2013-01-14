from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from datetime import datetime
from django.views.generic import DetailView, TemplateView, ListView
from classes.models import Event, Registration, Bio, Session
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.template import Context
from django.contrib.auth.decorators import login_required
from email import send_registration_mail
from helpers import *
from django.db.models import Q

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
			
		return context
			


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
				["contact@knowledgecommonsdc.org"],
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
			message_text = "You've been registered"
		elif self.kwargs['slug'] == "waitlisted":
			message_text = "You've been added to the waitlist"
		elif self.kwargs['slug'] == "cancelled":
			message_text = "Registration cancelled"
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



# display a list of registrations for a given session
@login_required
class RegistrationListView(ListView):

	context_object_name = "registration_list"
	model = Registration
	
	def get_context_data(self, **kwargs):
		
		context = super(RegistrationListView, self).get_context_data(**kwargs)
		context['events'] = Registration.objects.filter(event__session__slug=self.kwargs['slug'])
		return context

