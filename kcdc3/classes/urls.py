from django.conf.urls import patterns, include, url
from classes.models import Event, Registration
from django.views.generic import ListView
from classes.views import EventDetailView

urlpatterns = patterns('classes.views',

	url(r'^$', ListView.as_view(model=Event,)),
	url(r'^(?P<slug>[A-Za-z0-9_-]+)/$', EventDetailView.as_view(model=Event,)),
	url(r'^(?P<slug>[A-Za-z0-9_-]+)/register$', 'register'),
	url(r'^(?P<slug>[A-Za-z0-9_-]+)/cancel$', 'cancel'),

)
