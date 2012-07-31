from django.conf.urls import patterns, include, url
from django.views.generic import ListView
from classes.models import Event, Registration

urlpatterns = patterns('classes.views',

	url(r'^$', ListView.as_view(model=Event,)),
	url(r'^(?P<slug>[A-Za-z0-9_-]+)/$', 'single'),
	url(r'^(?P<slug>[A-Za-z0-9_-]+)/register$', 'register'),

)
