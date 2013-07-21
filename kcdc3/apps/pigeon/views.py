from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import DetailView, TemplateView, ListView
from datetime import datetime
from django.template import Context
from django.db.models import Q
from django.contrib.syndication.views import Feed
from models import Post
from kcdc3.apps.classes.models import Bio



# display a list of posts
class PostListView(ListView):

	context_object_name = "post_list"
	model = Post
	
	def get_context_data(self, **kwargs):
		
		context = super(PostListView, self).get_context_data(**kwargs)
		context['posts'] = Post.objects.filter(status='PUBLISHED').exclude(date__gte=datetime.now()).order_by('-date')
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
			



# RSS feed
class BlogFeed(Feed):
	title = "KCDC Blog"
	link = "/blog/"
	description = "Knowledge Commons DC Blog"

	def items(self):
		return Post.objects.filter(status='PUBLISHED').exclude(date__gte=datetime.now()).order_by('-date')[:10]

	def item_title(self, item):
		return item.title

	def item_description(self, item):
		return item.teaser




