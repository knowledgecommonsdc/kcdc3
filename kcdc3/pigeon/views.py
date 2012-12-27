from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import DetailView, TemplateView, ListView
from datetime import datetime
from django.template import Context
from django.db.models import Q
from pigeon.models import Post
from classes.models import Bio



# display a list of posts
class PostListView(ListView):

	context_object_name = "post_list"
	model = Post
	
	def get_context_data(self, **kwargs):
		
		context = super(PostListView, self).get_context_data(**kwargs)
		context['posts'] = Post.objects.filter(status='PUBLISHED').exclude(date__gte=datetime.now())
		context['recent_posts'] = context['posts'][:15]

		return context




# display a list of posts for a particular month
class PostArchiveView(ListView):

	context_object_name = "post_list"
	model = Post
	
	def get_context_data(self, **kwargs):

		# convert slug into date: remarkable thing, this datetime object
		target_date = datetime.strptime(self.kwargs['date_slug'], '%y%m')
		
		context = super(PostArchiveView, self).get_context_data(**kwargs)
		context['posts'] = Post.objects.filter(status='PUBLISHED').exclude(date__gte=datetime.now())
		context['recent_posts'] = context['posts'].filter(date__year=target_date.year).filter(date__month=target_date.month)

		return context



# display a single post	
class PostDetailView(DetailView):

	context_object_name = "post"
	model = Post
	
	def get_context_data(self, **kwargs):
		
		context = super(PostDetailView, self).get_context_data(**kwargs)
		context['posts'] = Post.objects.filter(status='PUBLISHED').exclude(date__gte=datetime.now())
		return context
			
