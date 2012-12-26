from django.db import models
import datetime



class Page(models.Model):
	title = models.CharField(max_length=200)
	short_title = models.CharField(max_length=32)
	STATUS_CHOICES = (
		('PUBLISHED', 'Published'),
		('HIDDEN', 'Hidden'),
		('DRAFT', 'Draft'),
		('REMOVED', 'Removed'),
	)
	status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='CURRENT')
	featured = models.BooleanField(default=False)

	path = models.CharField(max_length=200, unique=True)
	parent = models.ForeignKey('self', null=True,blank=True)

	teaser = models.TextField(blank=True)
	main_text = models.TextField(blank=True)
	sidebar_text = models.TextField(blank=True)

	class Meta:
		ordering = ['path']

	def __unicode__(self):
		return self.title


