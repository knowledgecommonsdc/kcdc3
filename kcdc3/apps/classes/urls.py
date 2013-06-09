from django.conf.urls import patterns, include, url
from models import Event, Registration
from views import EventListView, EventDetailView, ResponseTemplateView, EventArchiveView, SessionView, RegistrationListView

urlpatterns = patterns('kcdc3.apps.classes.views',

	url(r'^$', EventListView.as_view()),
	url(r'^dashboard/registrations/(?P<slug>[A-Za-z0-9_-]+)$', RegistrationListView.as_view()),
	url(r'^(?P<slug>[0-9_-]+)/$', EventArchiveView.as_view()),
	url(r'^(?P<slug>[0-9_-]+)/background/$', SessionView.as_view()),
	url(r'^response/(?P<slug>[A-Za-z0-9_-]+)$', ResponseTemplateView.as_view()),
	url(r'^(?P<slug>[A-Za-z0-9_-]+)/$', EventDetailView.as_view(model=Event,)),
	url(r'^(?P<slug>[A-Za-z0-9_-]+)/register$', 'register'),
	url(r'^(?P<slug>[A-Za-z0-9_-]+)/cancel$', 'cancel'),
	url(r'^(?P<slug>[A-Za-z0-9_-]+)/facilitator$', 'facilitator'),

)
