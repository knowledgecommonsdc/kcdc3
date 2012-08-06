from django.http import HttpRequest, HttpResponseRedirect
from datetime import datetime
from django.views.generic import DetailView, TemplateView, ListView
from classes.models import Event, Registration
from django.core.mail import send_mail
from django.template.loader import render_to_string


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
		context['registration_count'] = r.registration_count
		context['waitlist_count'] = r.waitlist_count
		context['user_is_waitlisted'] = r.user_is_waitlisted
		context['user_is_registered'] = r.user_is_registered
		context['is_registration_open'] = r.is_registration_open
		context['add_to_waitlist'] = r.add_to_waitlist
				
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
			message_body = render_to_string('classes/email_registered.txt', {'title': e.title})
			send_mail("Registered: "+e.title, message_body, 'contact@knowledgecommonsdc.org', [request.user.email], fail_silently=False)
			return HttpResponseRedirect("/classes/response/registered")
		else:
			message_body = render_to_string('classes/email_registered.txt', {'title': e.title})
			send_mail(e.title, message_body, 'contact@knowledgecommonsdc.org', [request.user.email], fail_silently=False)
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
				message_body = render_to_string('classes/email_promoted.txt', {'title': e.title})
				recipient = w.student.email
				send_mail("You've been registered: "+e.title, message_body, 'contact@knowledgecommonsdc.org', [recipient], fail_silently=False)
		message_body = render_to_string('classes/email_registered.txt', {'title': e.title})
		send_mail("Registration cancelled: "+e.title, message_body, 'contact@knowledgecommonsdc.org', [request.user.email], fail_silently=False)
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
class FacilitatorEventDetailView(EventDetailView):

	template_name = "classes/facilitator_event_detail.html"

	def get_context_data(self, **kwargs):
		
		context = super(EventDetailView, self).get_context_data(**kwargs)

		r = RegistrationHelper(self.object)
		context['registration_count'] = r.registration_count
		context['waitlist_count'] = r.waitlist_count

		e = self.object
		context['registered_students'] = Registration.objects.filter(event=self.object, waitlist=False, cancelled=False)
		context['waitlisted_students'] = Registration.objects.filter(event=self.object, waitlist=True, cancelled=False)

		return context



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
		if self.e.registration_status == 'ALLOW' or self.e.registration_status == 'AUTO':
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
		if self.e.registration_status == 'ALLOW' or self.e.registration_status == 'AUTO':
			self.is_registration_open = True
		else: 
			self.is_registration_open = False

