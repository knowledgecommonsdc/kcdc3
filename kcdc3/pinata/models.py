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
	sort_order = models.IntegerField(blank=True, null=True, default=50)

	path = models.CharField(max_length=200, unique=True)
	parent = models.ForeignKey('self', null=True,blank=True)

	teaser = models.TextField(blank=True)
	main_text = models.TextField(blank=True)
	sidebar_text = models.TextField(blank=True)

	class Meta:
		ordering = ['path']

	def __unicode__(self):
		return self.title



class Notice(models.Model):
	""" Short-term notices that appear on the front page """

	title = models.CharField(max_length=200)
	main_text = models.TextField(blank=True)
	live = models.BooleanField(default=True)
	sort_order = models.IntegerField(blank=True, null=True, default=50)

	class Meta:
		ordering = ['sort_order']
		verbose_name=u'Front Page Notice'

	def __unicode__(self):
		return self.title
	


class Slide(models.Model):
	""" Slides for the front page """

	title = models.CharField(max_length=200)
	main_text = models.TextField(blank=True)
	image = models.ImageField('Image (960x360px)', upload_to='front_slides', blank=True, null=True)
	live = models.BooleanField(default=True)
	sort_order = models.IntegerField(blank=True, null=True, default=50)

	class Meta:
		ordering = ['sort_order']
		verbose_name=u'Front Page Slide'

	def __unicode__(self):
		return self.title
	

