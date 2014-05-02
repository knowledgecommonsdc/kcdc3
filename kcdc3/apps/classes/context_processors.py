from django.conf import settings

# Make values from global settings available
def global_settings(request):
	
	return {
		'PROJECT_NAME': settings.PROJECT_NAME,
		'PROJECT_SHORT_NAME': settings.PROJECT_SHORT_NAME,
		'PROJECT_EMAIL': settings.PROJECT_EMAIL,
	}
	
	