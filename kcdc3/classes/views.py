from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from datetime import datetime
from django.views.generic import DetailView, TemplateView, ListView
from classes.models import Event, Registration, Bio
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.template import Context
from django.contrib.auth.decorators import login_required
from email import send_registration_mail
from helpers import *

# display a list of events
class EventListView(ListView):

	context_object_name = "event_list"
	model = Event
	
	def get_context_data(self, **kwargs):
		
		context = super(EventListView, self).get_context_data(**kwargs)

		return context


	
# display a single event	
class EventDetailView(DetailView):

	context_object_name = "event"
	model = Event
	
	def get_context_data(self, **kwargs):
		
		context = super(EventDetailView, self).get_context_data(**kwargs)

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
		if waitlist_status == False:
			send_registration_mail(e, 'registered', request.user.email)
			return HttpResponseRedirect("/classes/response/registered")
		else:
			send_registration_mail(e, 'waitlisted', request.user.email)
			return HttpResponseRedirect("/classes/response/waitlisted")

		# Email us with the needs of the student.
		if request.GET["student_needs"] != "":
			send_mail(e.title + " Student Considerations",
				"Student requested the following: "+request.GET["student_needs"],
				"contact@knowledgecommonsdc.org",
				["contact@knowledgecommonsdc.org"],
				fail_silently=False)
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
