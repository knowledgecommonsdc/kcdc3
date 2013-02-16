from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from datetime import datetime
from django.template import Context
from django.db.models import Q
from pinata.models import Page
from classes.models import Bio, Role


def page_view(request):

	# debug
	print('path: "'+request.path+'"')	

	# Remove trailing slashes from incoming path.
	# Probably best handled in urls.py,
	# and there is probably a more future-proof way of doing this.
	search_path = request.path.rstrip('/')

	# debug
	# print('search path: "'+search_path+'"')	

	e = Page.objects.get(path=search_path)
	context = Context()
	
	context['title'] = e.title
	context['short_title'] = e.short_title
	context['id'] = e.id
	context['path'] = e.path
	context['teaser'] = e.teaser
	context['main_text'] = e.main_text
	context['sidebar_text'] = e.sidebar_text
	context['parent'] = e.parent

	# get all other pages with the same parent
	if e.parent:
		context['siblings'] = Page.objects.filter(Q(parent=e.parent)&Q(status='PUBLISHED')).order_by('sort_order', 'path',)
		
	# get all children
	context['children'] = Page.objects.filter(Q(parent=e)&Q(status='PUBLISHED')).order_by('sort_order', 'path',)
		
	if e.status == 'PUBLISHED' or e.status == 'HIDDEN':
		return render_to_response('pinata/page.html',context)
	else:
		raise Http404
		
		
		
def staff(request):
	
	context = Context()

	e = Page.objects.get(path='/about')
	print(e.main_text)
	context['main_text'] = e.main_text
	
	context['dojo'] = Bio.objects.filter(role__name='Dojo')
	context['volunteers'] = Bio.objects.filter(role__name='Volunteers')
	context['dojo_at_large'] = Bio.objects.filter(role__name='Dojo-at-Large')
	context['dojo_emeritus'] = Bio.objects.filter(role__name='Dojo Emeritus')

	context['dojo_role'] = Role.objects.get(name='Dojo')
	context['volunteers_role'] = Role.objects.get(name='Volunteers')
	context['dojo_at_large_role'] = Role.objects.get(name='Dojo-at-Large')
	context['dojo_emeritus_role'] = Role.objects.get(name='Dojo Emeritus')

	# get all other pages with the same parent
	if e.parent:
		context['siblings'] = Page.objects.filter(Q(parent=e.parent)&Q(status='PUBLISHED')).order_by('sort_order', 'path',)
		
	# get all children
	context['children'] = Page.objects.filter(Q(parent=e)&Q(status='PUBLISHED')).order_by('sort_order', 'path',)

	return render_to_response('pinata/staff.html',context)
