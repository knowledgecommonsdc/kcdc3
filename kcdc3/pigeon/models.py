from django.db import models
from classes.models import Bio
import datetime



class Post(models.Model):

	title = models.CharField(max_length=200)
	slug = models.SlugField(unique=True)
	STATUS_CHOICES = (
		('PUBLISHED', 'Published'),
		('HIDDEN', 'Hidden'),
		('DRAFT', 'Draft'),
		('REMOVED', 'Removed'),
	)
	status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='CURRENT')
	featured = models.BooleanField(default=False)
	date = models.DateTimeField()

	thumbnail = models.ImageField(upload_to='post_images', blank=True, null=True)
	teaser = models.TextField(blank=True)
	main_text = models.TextField(blank=True)

	author = models.ManyToManyField(Bio, blank=True, null=True, related_name='author')
	tags = models.CharField(max_length=128, blank=True)
	allow_comments = models.BooleanField(default=True)

	class Meta:
		ordering = ['date']

	def __unicode__(self):
		return self.title


