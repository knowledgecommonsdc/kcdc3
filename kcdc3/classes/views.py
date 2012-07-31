from django.shortcuts import render_to_response
from django.http import HttpRequest
from datetime import datetime
from classes.models import Event, Registration

def index(request):
	class_list = Event.objects.all().order_by('date')
	return render_to_response('classes/index.html', {'class_list': class_list})
	
def single(request, slug):
	event = Event.objects.get(slug=slug)
	registration_count = Event.objects.filter(slug=slug, registration__waitlist=False, registration__cancelled=False).count()
	waitlist_count = Event.objects.filter(slug=slug, registration__waitlist=True, registration__cancelled=False).count()
	return render_to_response('classes/single.html', {'event': event, 'registration_count': registration_count, 'waitlist_count': waitlist_count})
	
def register(request, slug):
	event = Event.objects.get(slug=slug)
	r = Registration(student=request.user, event=event, date_registered=datetime.now(), waitlist=False)
	r.save()
	return render_to_response('classes/register-response.html', {'event': event})
	
