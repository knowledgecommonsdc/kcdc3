from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from datetime import datetime
from django.template import RequestContext
from django.views.generic import DetailView, TemplateView, ListView
from django.db.models import Q
from models import Page, Notice, Slide, Sponsor, PressClipping
from kcdc3.apps.classes.models import Bio, Role, Event, Session
from kcdc3.apps.pigeon.models import Post


def page_view(request):
	""" Handle requests for pages. """

	context = RequestContext()
	context['user'] = request.user

	# debug
	# print('path: "'+request.path+'"')	

	# Remove trailing slashes from incoming path.
	# Probably best handled in urls.py,
	# and there is probably a more future-proof way of doing this.
	search_path = request.path.rstrip('/')

	# debug
	# print('search path: "'+search_path+'"')	

	e = Page.objects.get(path=search_path)
	
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
	
	# set up templates
	template_path = 'pinata/' + e.template
		
	if e.status == 'PUBLISHED' or e.status == 'HIDDEN':
		return render_to_response(template_path, context, context_instance=RequestContext(context))
	else:
		raise Http404
		


def staff(request):
	""" Front page of the About section.
	Includes staff and volunteer listings. """

	""" TODO: This really ought to be a class-based view """

	context = Context()
	context['user'] = request.user

	e = Page.objects.get(path='/about')
	print(e.main_text)
	context['main_text'] = e.main_text
	context['short_title'] = e.short_title
	context['title'] = e.title
	
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
		
	# todo: rewrite this so it returns section home and subpages
	# todo: write new function that returns children only for non-section-homes
		
	# get all children
	context['children'] = Page.objects.filter(Q(parent=e)&Q(status='PUBLISHED')).order_by('sort_order', 'path',)

	return render_to_response('pinata/staff.html',context)



def home(request):
	""" Sitewide home page """

	context = Context()
	context['user'] = request.user

	# Get information for front page content
	context['notices'] = Notice.objects.filter(live=True)
	context['slides'] = Slide.objects.filter(live=True)
		
	# Pull content from elsewhere in the site
	context['events'] = Event.objects.filter(status='PUBLISHED', session__status="CURRENT", featured=True).order_by('date')[:4]
	context['posts'] = Post.objects.filter(status='PUBLISHED').filter(featured=True).exclude(date__gte=datetime.now())[:4]

	return render_to_response('pinata/home.html',context)




def proposal(request):
	""" Course proposal page """
	
	""" TODO: The observant reader may note that this method 
	is identical to contribute(), except for the template name. 
	Really, though, it would be best to modify page_view() and 
	Page so that admins could choose a template on the backend. """
	
	context = Context()
	context['user'] = request.user

	e = Page.objects.get(path='/teach/proposal')
	print(e.main_text)
	context['main_text'] = e.main_text
	context['short_title'] = e.short_title
	context['title'] = e.title
	context['id'] = e.id

	# get all other pages with the same parent
	if e.parent:
		context['siblings'] = Page.objects.filter(Q(parent=e.parent)&Q(status='PUBLISHED')).order_by('sort_order', 'path',)
		
	# get all children
	context['children'] = Page.objects.filter(Q(parent=e)&Q(status='PUBLISHED')).order_by('sort_order', 'path',)

	return render_to_response('pinata/proposal.html',context)





def partners(request):
	""" List of sponsors. """

	""" TODO: This really ought to be a class-based view """

	context = Context()
	context['user'] = request.user

	e = Page.objects.get(path='/about/partners')
	print(e.main_text)
	context['main_text'] = e.main_text
	context['short_title'] = e.short_title
	context['title'] = e.title
	context['id'] = e.id
	
	context['sponsors_A'] = Sponsor.objects.filter(group='A').filter(status='PUBLISHED')
	context['sponsors_B'] = Sponsor.objects.filter(group='B').filter(status='PUBLISHED')
	context['sponsors_S'] = Sponsor.objects.filter(group='S').filter(status='PUBLISHED')
	
	# get all other pages with the same parent
	if e.parent:
		context['siblings'] = Page.objects.filter(Q(parent=e.parent)&Q(status='PUBLISHED')).order_by('sort_order', 'path',)
		
	# get all children
	context['children'] = Page.objects.filter(Q(parent=e)&Q(status='PUBLISHED')).order_by('sort_order', 'path',)

	return render_to_response('pinata/partners.html',context)




def pressclippings(request):
	""" List of press clippings. """

	""" TODO: This really ought to class-based view """

	context = Context()
	context['user'] = request.user

	e = Page.objects.get(path='/press')
	print(e.main_text)
	context['main_text'] = e.main_text
	context['short_title'] = e.short_title
	context['title'] = e.title
	context['id'] = e.id
	
	context['pressclippings'] = PressClipping.objects.filter(status='PUBLISHED')
	
	# get all other pages with the same parent
	if e.parent:
		context['siblings'] = Page.objects.filter(Q(parent=e.parent)&Q(status='PUBLISHED')).order_by('sort_order', 'path',)
		
	# get all children
	context['children'] = Page.objects.filter(Q(parent=e)&Q(status='PUBLISHED')).order_by('sort_order', 'path',)

	return render_to_response('pinata/pressclippings.html',context)



