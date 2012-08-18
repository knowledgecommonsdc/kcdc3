from django.conf.urls.defaults import *
from accounts.views import SignupFormExtra
from filebrowser.sites import site

# development
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

	url(r'^classes/', include('classes.urls')),
	url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
	url(r'^accounts/signup/$', 'userena.views.signup', {'signup_form': SignupFormExtra}),
	url(r'^accounts/', include('userena.urls')),

)

# development
urlpatterns += staticfiles_urlpatterns()
