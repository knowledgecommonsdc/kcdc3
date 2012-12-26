from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from datetime import datetime
from django.template import Context
from django.http import Http404
from django.db.models import Q
from pinata.models import Page



def page_view(request, path):

	# Remove trailing slashes from incoming path.
	# Probably best handled in urls.py,
	# and there is probably a more future-proof way of doing this.
	path = path.rstrip('/')

	# print('path: "'+path+'"')	

	e = Page.objects.get(path=path)
	context = Context()
	
	context['title'] = e.title
	context['short_title'] = e.short_title
	context['teaser'] = e.teaser
	context['main_text'] = e.main_text
	context['sidebar_text'] = e.sidebar_text
	context['parent'] = e.parent

	# get all other pages with the same parent
	context['siblings'] = Page.objects.filter(Q(parent=e.parent)&Q(status='PUBLISHED'))
		
	if e.status == 'PUBLISHED' or e.status == 'HIDDEN':
		return render_to_response('pinata/page.html',context)
	else:
		raise Http404
		
		