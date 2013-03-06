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
	status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='PUBLISHED')
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
		ordering = ['sort_order','title']
		verbose_name=u'Front Notice'

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
		ordering = ['sort_order','title']
		verbose_name=u'Front Slide'

	def __unicode__(self):
		return self.title
	


class Sponsor(models.Model):
	""" Sponsor and partner organizations """

	title = models.CharField(max_length=200)
	main_text = models.TextField(blank=True)
	image = models.ImageField('Image', upload_to='sponsors', blank=True, null=True)
	destination_url = models.URLField(blank=True)
	GROUP_CHOICES = (
		('A', 'Major Partner'),
		('B', 'Minor Partner'),
		('S', 'Space'),
	)
	group = models.CharField(max_length=3, choices=GROUP_CHOICES, default='B')

	STATUS_CHOICES = (
		('PUBLISHED', 'Published'),
		('HIDDEN', 'Hidden'),
		('DRAFT', 'Draft'),
		('REMOVED', 'Removed'),
	)
	status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='PUBLISHED')
	sort_order = models.IntegerField(blank=True, null=True, default=50)

	class Meta:
		ordering = ['group','sort_order','title']

	def __unicode__(self):
		return self.title




class PressClipping(models.Model):
	""" A press article """

	title = models.CharField(max_length=200)
	main_text = models.TextField(blank=True)
	date = models.DateField(blank=True)
	publication = models.CharField(max_length=200,blank=True)
	excerpt = models.TextField(blank=True)
	destination_url = models.URLField(blank=True)

	STATUS_CHOICES = (
		('PUBLISHED', 'Published'),
		('HIDDEN', 'Hidden'),
		('DRAFT', 'Draft'),
		('REMOVED', 'Removed'),
	)
	status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='PUBLISHED')

	class Meta:
		ordering = ['date']
		verbose_name=u'Press Clipping'

	def __unicode__(self):
		return self.title
