from django.db import models
from django.contrib.contenttypes import generic
from django.core.exceptions import ValidationError
from common.media.models import Image, Video, Audio, File
from tagging.models import Tag
from django.conf import settings
# UK Based at the moment
from django.contrib.localflavor.uk import forms
# import UKPostcodeField

from common.api import google, isgd

class CommonVenue(models.Model):
  name = models.CharField(max_length=65, unique=True)
  address = models.TextField()
  city = models.CharField(max_length=65)
  # Need to validate
  postcode = models.CharField(max_length=8)
  email = models.EmailField(max_length=255)
  # Needs work to validate telephone number:
  # http://www.djangosnippets.org/snippets/1207/ Looks useable
  telephone = models.CharField(max_length=16)
  website = models.URLField(max_length=255)
  images = generic.GenericRelation(Image)
  latitude = models.FloatField(editable=False, blank=True, null=True)
  longitude = models.FloatField(editable=False, blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  class Meta:
      ordering = ['name']
      abstract = True
      
    
  def __unicode__(self):
    return self.name
      
  def save(self):
    google.geolocate(self)
    super(CommonVenue, self).save()
    
class CommonPerformer(models.Model):
  name = models.CharField(max_length=255)
  slug = models.SlugField(max_length=255, editable=False, null=True, blank=True)
  description = models.TextField(null=True, blank=True)
  email = models.EmailField(max_length=255, null=True, blank=True)
  website = models.URLField(max_length=255, null=True, blank=True)
  tags = models.ManyToManyField(Tag, null=True, blank=True)
  images = generic.GenericRelation(Image)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  class Meta:
    ordering = ['name']
    abstract = True
    
  @models.permalink # Decorator makes sure get_absolute_url returns a string rather than the full object!
  def get_permalink(self):
    return ('performer_detail', (), {
      "slug": self.slug,
    })
    
  def add_slug(self):
    from django.template.defaultfilters import slugify
    if self.name:
      self.slug = slugify(self.name)
    else:
      self.slug = slugify("%s - %s" % self.name)
  
  def __unicode__(self):
    return self.name
    
  def save(self):
    self.add_slug()
    super(CommonPerformer, self).save()

class CommonEvent(models.Model):
  slug = models.SlugField(max_length=255, editable=False, null=True, blank=True)
  name = models.CharField(max_length=65, null=True, blank=True)
  description = models.TextField(null=True, blank=True)
  link = models.URLField(null=True, blank=True)
  # DateTime breaking Admin....?
  start_date = models.DateField()
  end_date = models.DateField()
  images = generic.GenericRelation(Image)
  isgd = models.URLField(verify_exists=False, max_length=255, null=True, blank=True, editable = False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  class Meta:
    abstract = True
  
  @models.permalink # Decorator makes sure get_absolute_url returns a string rather than the full object!
  def get_permalink(self):
    return ('event_detail', (), {
      "event_id": self.id,
    })
    
  def clean(self):
    # Check end date is after start date
    if self.end_date < self.start_date:
      raise ValidationError('The end date must be later than the start date')
    
  def __unicode__(self):
    return self.name
    
  def save(self):
    isgd.shorten_url(self)
    super(CommonEvent, self).save()
