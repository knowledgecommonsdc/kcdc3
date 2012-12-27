from django.conf.urls import patterns, include, url
from pigeon.models import Post
from pigeon.views import PostListView, PostArchiveView, PostDetailView

urlpatterns = patterns('pigeon.views',

	url(r'^$', PostListView.as_view()),
	url(r'^(?P<date_slug>[0-9_-]+)/$', PostArchiveView.as_view()),
	url(r'^(?P<slug>[A-Za-z0-9_-]+)/$', PostDetailView.as_view(model=Post,)),

)
