from django.conf.urls import patterns, include, url
from models import Page

urlpatterns = patterns('kcdc3.apps.pinata.views',

	url(r'^$', 'page_view'),
	url(r'^[0-9a-zA-Z_-]+/$', 'page_view'),

)
