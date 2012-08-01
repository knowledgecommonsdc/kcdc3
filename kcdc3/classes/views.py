from django.http import HttpRequest, HttpResponseRedirect
from datetime import datetime
from django.views.generic import DetailView
from classes.models import Event, Registration


	
# display an event	
class EventDetailView(DetailView):

	context_object_name = "event"
	model = Event
	
	def get_context_data(self, **kwargs):
		
		context = super(EventDetailView, self).get_context_data(**kwargs)
		context['registration_count'] = Registration.objects.filter(event=self.object, waitlist=False, cancelled=False).count()
		context['waitlist_count'] = Registration.objects.filter(event=self.object, waitlist=True, cancelled=False).count()

		if (Registration.objects.filter(event=self.object, student=self.request.user, waitlist=True, cancelled=False).count() > 0):
			context['user_is_waitlisted'] = True
		else:
			context['user_is_waitlisted'] = False

		if (Registration.objects.filter(event=self.object, student=self.request.user, waitlist=False, cancelled=False).count() > 0):
			context['user_is_registered'] = True
		else:
			context['user_is_registered'] = False

		return context
			


# handle registration/waitlist form
def register(request, slug):
	
	e = Event.objects.get(slug=slug)
	r = RegistrationHelper(e,request.user)

	# if there are no non-cancelled registrations for this user and event
	if r.user_is_registered==False and r.user_is_waitlisted==False:
		t = Registration(student=request.user, event=e, date_registered=datetime.now(), waitlist=r.add_to_waitlist)
		t.save()
		if r.add_to_waitlist == False:
			return HttpResponseRedirect("/classes/registered")
		else:
			return HttpResponseRedirect("/classes/waitlisted")
	else: 
		return HttpResponseRedirect("/classes/error")



# handle cancel form
def cancel(request, slug):
	
	e = Event.objects.get(slug=slug)
	r = RegistrationHelper(e,request.user)
	
	if r.user_is_registered or r.user_is_waitlisted:
		for t in Registration.objects.filter(event=e, student=request.user, cancelled=False)[:1]:
			t.date_cancelled=datetime.now()
			t.cancelled=True
			t.save()
		if r.add_to_waitlist==True and e.waitlist_status==True:
		 	for w in Registration.objects.filter(event=e, waitlist=True, cancelled=False)[:1]:
				w.waitlist=False
				w.save()
		return HttpResponseRedirect("/classes/cancelled")
	else: 
		return HttpResponseRedirect("/classes/error")


# provide information about an event's registration status
# relative to a particular event and user
class RegistrationHelper:
		
	def __init__(self, event, student):

		self.e = event
		self.s = student

		registration_count = Registration.objects.filter(event=self.e, waitlist=False, cancelled=False).count()
		waitlist_count = Registration.objects.filter(event=self.e, waitlist=True, cancelled=False).count()

		if registration_count >= self.e.max_students:
			self.add_to_waitlist = True
		else:
			self.add_to_waitlist = False

		self.user_is_waitlisted = False
		self.user_is_registered = False
		if (Registration.objects.filter(event=self.e, student=self.s, waitlist=False, cancelled=False).count() > 0):
			self.user_is_registered = True
		elif (Registration.objects.filter(event=self.e, student=self.s, waitlist=True, cancelled=False).count() > 0):
			self.user_is_waitlisted = True
	
	
	