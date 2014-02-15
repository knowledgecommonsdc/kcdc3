from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from datetime import datetime
from django.views.generic import DetailView, TemplateView, ListView
from django.template.loader import render_to_string
from django.template import Context
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from models import Meeting, Meeting_Registration
from kcdc3.apps.classes.models import Bio
from helpers import *




# display a list of meetings
class MeetingListView(ListView):

	context_object_name = "meeting_list"
	model = Meeting
	
	def get_context_data(self, **kwargs):
		
		context = super(MeetingListView, self).get_context_data(**kwargs)
		context['meetings'] = Meeting.objects.filter(status='PUBLISHED')
		return context

	
# display a single meeting	
# Any user who knows the URL should be able to view and sign up.
# TODO restrict names and emails to staff
class MeetingDetailView(DetailView):

	context_object_name = "meeting"
	model = Meeting
	
	def get_context_data(self, **kwargs):
		
		context = super(MeetingDetailView, self).get_context_data(**kwargs)

		if self.request.user.is_authenticated():
			context['user_is_authenticated'] = True
			user = self.request.user
		else:
			user = None

		meeting = self.get_object()
			
		context['registration_count'] = meeting.registration_count()
		context['user_is_registered'] = is_registered(user, meeting)

		context['registrations'] = Meeting_Registration.objects.filter(meeting=self.get_object(), cancelled=False)

		# TODO: move this
		if self.request.user.is_authenticated():
			if self.request.user.is_staff:
				context['show_contacts'] = True
			
		if meeting.status == 'PUBLISHED' or meeting.status == 'HIDDEN':
			return context
		else:
			raise Http404
						


# handle registration form
def register(request, slug):

	e = Meeting.objects.get(slug=slug)
	u = request.user
	if request.POST["note"]:
		n = request.POST["note"]
	else:
		n = ""

	# go ahead and register this person
	# no need to check registration status
	t = Meeting_Registration(user=u, 
		meeting=e, 
		note=n,
		date_registered=datetime.now())
	t.save()
	return HttpResponseRedirect("/staff/response/registered")



# handle cancel form
def cancel(request, slug):
	
	e = Meeting.objects.get(slug=slug)
	
	if not is_cancelled(request.user, e) and is_registered(request.user, e):
		cancel_registration(request.user, e)
		return HttpResponseRedirect("/staff/response/cancelled")
	else: 
		return HttpResponseRedirect("/staff/response/error")



# redirect the user to a thank you/results sceen after they take an action
class ResponseTemplateView(TemplateView):

	template_name = "squirrel/response.html"
	 
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



