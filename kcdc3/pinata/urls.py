from django.conf.urls import patterns, include, url
from pinata.models import Page

urlpatterns = patterns('pinata.views',

	# right now, URLs are handled in the sitewide urls.py
	# TODO move handling into this file
	url(r'^(?P<path>^.*)', 'page_view'),

)
