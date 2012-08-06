from django.conf.urls import patterns, include, url
from classes.models import Event, Registration
from classes.views import EventListView, EventDetailView, ResponseTemplateView, FacilitatorEventDetailView

urlpatterns = patterns('classes.views',

	url(r'^$', EventListView.as_view()),
	url(r'^response/(?P<slug>[A-Za-z0-9_-]+)$', ResponseTemplateView.as_view()),
	url(r'^(?P<slug>[A-Za-z0-9_-]+)/$', EventDetailView.as_view(model=Event,)),
	url(r'^(?P<slug>[A-Za-z0-9_-]+)/register$', 'register'),
	url(r'^(?P<slug>[A-Za-z0-9_-]+)/cancel$', 'cancel'),
	url(r'^(?P<slug>[A-Za-z0-9_-]+)/facilitator$', FacilitatorEventDetailView.as_view(model=Event,)),

)
