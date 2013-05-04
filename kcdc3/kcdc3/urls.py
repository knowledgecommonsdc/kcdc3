from django.conf.urls.defaults import *
from accounts.views import SignupFormExtra
from filebrowser.sites import site
from django.conf import settings

# development
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

	url(r'^$', 'pinata.views.home'),
	url(r'^classes/', include('classes.urls')),
	url(r'^blog/', include('pigeon.urls')),
	url(r'^contribute/$', 'pinata.views.contribute'),
	url(r'^teach/proposal/$', 'pinata.views.proposal'),
	url(r'^about/$', 'pinata.views.staff'),
	url(r'^about/sponsors/$', 'pinata.views.sponsors'),
	url(r'^press/$', 'pinata.views.pressclippings'),
	url(r'^about/|teach/|contribute/', include('pinata.urls')),
	url(r'^admin/filebrowser/', include(site.urls)),
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^grappelli/', include('grappelli.urls')),
	url(r'^accounts/signup/$', 'userena.views.signup', {'signup_form': SignupFormExtra}),
	url(r'^accounts/', include('userena.urls')),

)


if settings.DEBUG:
	urlpatterns += patterns('',
		url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
			'document_root': settings.MEDIA_ROOT,
		}),
		url(r'^assets/(?P<path>.*)$', 'django.views.static.serve', {
			'document_root': settings.ASSETS_ROOT,
		}),
   )
