from django.conf.urls import patterns, include, url
from models import Meeting
from views import MeetingListView, MeetingDetailView, ResponseTemplateView

urlpatterns = patterns('kcdc3.apps.squirrel.views',

	url(r'^$', 'home'),
	url(r'^meetings/$', MeetingListView.as_view()),
	url(r'^response/(?P<slug>[A-Za-z0-9_-]+)$', ResponseTemplateView.as_view()),
	url(r'^meetings/(?P<slug>[A-Za-z0-9_-]+)/$', MeetingDetailView.as_view(model=Meeting,)),
	url(r'^meetings/(?P<slug>[A-Za-z0-9_-]+)/register$', 'register'),
	url(r'^meetings/(?P<slug>[A-Za-z0-9_-]+)/cancel$', 'cancel'),
	url(r'^response/(?P<slug>[A-Za-z0-9_-]+)$', ResponseTemplateView.as_view()),

)
