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
			r = UserRegistrationHelper(self.object,self.request.user)
		else:
			r = RegistrationHelper(self.object)
		context['registration_count'] = self.get_object().registration_count()
		context['waitlist_count'] = self.get_object().waitlist_count()
		context['user_is_waitlisted'] = r.user_is_waitlisted
		context['user_is_registered'] = r.user_is_registered
		context['is_registration_open'] = r.is_registration_open
		context['add_to_waitlist'] = r.add_to_waitlist

		# TODO: move this
		if self.request.user.is_authenticated():
			if Event.objects.filter(slug=self.object.slug, facilitators=self.request.user).count() > 0 or self.request.user.is_staff:
				context['show_facilitator'] = True
			
		return context
			


# handle registration/waitlist form
def register(request, slug):

	e = Event.objects.get(slug=slug)
	r = UserRegistrationHelper(e,request.user)

	# if there are no non-cancelled registrations for this user/event and registration is possible
	if r.user_is_registered==False and r.user_is_waitlisted==False and r.is_registration_open==True:
		t = Registration(student=request.user, event=e, date_registered=datetime.now(), waitlist=r.add_to_waitlist)
		t.save()
		if r.add_to_waitlist == False:
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
	r = UserRegistrationHelper(e,request.user)
	
	if r.user_is_registered or r.user_is_waitlisted:
		for t in Registration.objects.filter(event=e, student=request.user, cancelled=False)[:1]:
			t.date_cancelled=datetime.now()
			t.cancelled=True
			t.save()
		if r.add_to_waitlist==True and e.waitlist_status==True:
		 	for w in Registration.objects.filter(event=e, waitlist=True, cancelled=False)[:1]:
				w.waitlist=False
				w.save()
				send_registration_mail(e, 'promoted', w.student.email)
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
	r = RegistrationHelper(e)

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


# provide information about all registrations for an event
# TODO much of this should probably be in the model
class RegistrationHelper:
		
	def __init__(self, event):

		self.e = event

		self.registration_count = Registration.objects.filter(event=self.e, waitlist=False, cancelled=False).count()
		self.waitlist_count = Registration.objects.filter(event=self.e, waitlist=True, cancelled=False).count()

		if self.registration_count >= self.e.max_students:
			self.add_to_waitlist = True
		else:
			self.add_to_waitlist = False	
	
		self.user_is_waitlisted = False
		self.user_is_registered = False
		
		# TODO - account for time offsets and session-wide control in automatically opening registration
 		if self.e.date < datetime.now():
			self.is_registration_open = False
		elif self.e.registration_status == 'ALLOW':
			self.is_registration_open = True
		elif self.e.registration_status == 'AUTO' and self.e.session.registration_status == 'ALLOW':
			self.is_registration_open = True
		else: 
			self.is_registration_open = False
		
		
# provide information about an event's registration status
# relative to a particular event and user
# TODO remove repetitive code in __init__
class UserRegistrationHelper(RegistrationHelper):

	def __init__(self, event, student):

		self.e = event
		self.s = student

		self.registration_count = Registration.objects.filter(event=self.e, waitlist=False, cancelled=False).count()
		self.waitlist_count = Registration.objects.filter(event=self.e, waitlist=True, cancelled=False).count()

		if self.registration_count >= self.e.max_students:
			self.add_to_waitlist = True
		else:
			self.add_to_waitlist = False	

		self.user_is_waitlisted = False
		self.user_is_registered = False
		if (Registration.objects.filter(event=self.e, student=self.s, waitlist=False, cancelled=False).count() > 0):
			self.user_is_registered = True
		elif (Registration.objects.filter(event=self.e, student=self.s, waitlist=True, cancelled=False).count() > 0):
			self.user_is_waitlisted = True

		# TODO - account for time offsets and session-wide control in automatically opening registration
 		if self.e.date < datetime.now():
			self.is_registration_open = False
		elif self.e.registration_status == 'ALLOW':
			self.is_registration_open = True
		elif self.e.registration_status == 'AUTO' and self.e.session.registration_status == 'ALLOW':
			self.is_registration_open = True
		else: 
			self.is_registration_open = False

# Another pain point in this file is the weird registartion helpers. These can
# be fixed by getting rid of the registartion helpers in general. Looks like
# the functionality is duplicated in models (specifically within the Event
# model). 
#
# The registration helpers do the following things:
#	For both UserRegistrationHelper and RegistrationHelper
#	* Helps to populate contexts for templates.
#
#	For UserRegistrationHelper:
#	* Checks to see if the user is registered for the event.
#	* Checks to see if the user is on the waitlist.
#	* Checks to see if the event is open for registration.
#	* Checks to see if the user should be added to the event's waitlist.
#	* Checks to see the number of users on the waitlist for a given event.
#	* Checks to see the number of users that are registered for a given event.
#
# The functionality of the registration helpers clearly breaks down into two
# different fields: user handling, and event status querying. 
#
# To deal with the event status querying, the event model itself should handle
# those questions. This is totally NBD.
#
# To deal with the context functionality we just peel shit out of the models.
# All the data the registration helpers provide can be found in the models.
# But there's still an open question about registration objects.
#
# There's weirdness with the user functionality that's rolled into the
# registration helpers. Users are accounts that are used on the site. When a
# user registeres for an event, it creates a registration object. This
# registration object contains the following:
#	* Keeps track of the user that registered.
#	* Keeps track of the event that the user is trying to register for.
#	* When the user was registered for that class.
#	* Whether the user is waitlisted for the event.
#	* Whether or not the user attended the event.
#	* Whether or not the user has cancelled their registration.
#	* And when they cancelled (if they did).
#
# There is literally nothing in the user model, nor in the user profile
# model (everything for users is contained in the Userina application).

# Logic can be cleaned up for the waitlist or not stuff. Not sure how yet. 
