from django.http import HttpRequest, HttpResponseRedirect
from datetime import datetime
from django.views.generic import DetailView
from classes.models import Event, Registration
	
	
	
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
			


def register(request, slug):
	
	e = Event.objects.get(slug=slug)
	registration_count = Registration.objects.filter(event=e, waitlist=False, cancelled=False).count()
	curr_user_registration_count = Registration.objects.filter(event=e, student=request.user, cancelled=False).count()

	if registration_count >= e.max_students:
		waitlist = True
	else:
		waitlist = False

	# if there are no non-cancelled registrations for this user and event
	if curr_user_registration_count == 0:
		r = Registration(student=request.user, event=e, date_registered=datetime.now(), waitlist=waitlist)
		r.save()
		if waitlist == False:
			return HttpResponseRedirect("/classes/registered")
		else:
			return HttpResponseRedirect("/classes/waitlisted")
	else: 
		return HttpResponseRedirect("/classes/error")



def cancel(request, slug):
	
	e = Event.objects.get(slug=slug)
	registration_count = Registration.objects.filter(event=e, waitlist=False, cancelled=False).count()
	curr_user_registration_count = Registration.objects.filter(event=e, student=request.user, cancelled=False).count()

	if registration_count >= e.max_students:
		waitlist = True
	else:
		waitlist = False

	if curr_user_registration_count > 0:
		for r in Registration.objects.filter(event=e, student=request.user, cancelled=False)[:1]:
			r.date_cancelled=datetime.now()
			r.cancelled=True
			r.save()
		if waitlist==True and r.waitlist==False:
		 	for n in Registration.objects.filter(event=e, waitlist=True, cancelled=False)[:1]:
				n.waitlist=False
				n.save()
		return HttpResponseRedirect("/classes/cancelled")
	else: 
		return HttpResponseRedirect("/classes/error")
