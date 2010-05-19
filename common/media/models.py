from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Image(models.Model):
  local_image = models.ImageField(upload_to="uploads/%Y/%m/%d/", height_field="height", width_field="width", max_length=255, null=True, blank=True)
  remote_image = models.CharField(editable=False, max_length=255, null=True, blank=True)
  thirdparty_page = models.CharField(editable=False, max_length=255, blank=True, null=True)
  size = models.CharField(editable=False, max_length=25, blank=True, null=True)
  content_type = models.ForeignKey(ContentType)
  object_id = models.PositiveIntegerField()
  content_object = generic.GenericForeignKey('content_type', 'object_id')
  height = models.PositiveIntegerField(editable=False, blank=True, null=True)
  width = models.PositiveIntegerField(editable=False, blank=True, null=True)
  created_at = models.DateTimeField(editable=False, auto_now_add=True)
  updated_at = models.DateTimeField(editable=False, auto_now=True)
  
  def save(self):
    """Store image locally if we have a URL"""
    import urllib
    import os
    from django.core.files import File

    if self.remote_image and not self.local_image:
      result = urllib.urlretrieve(self.remote_image)
      self.local_image.save(
        os.path.basename(self.remote_image),
        File(open(result[0]))
      )

    super(Image, self).save()
    
  
  def __unicode__(self):
    if self.local_image:
      return u'%s' % (self.local_image.name)
    else:
      return u'%s' % (self.remote_image)
      
class Video(models.Model):
  PROVIDER_CHOICES = (
    ('youtube', 'youtube.com'),
    ('vimeo', 'vimeo.com'),
  )
  url = models.URLField(max_length=255)
  provider = models.TextField(max_length=10, choices=PROVIDER_CHOICES)
  content_type = models.ForeignKey(ContentType)
  object_id = models.PositiveIntegerField()
  content_object = generic.GenericForeignKey('content_type', 'object_id')
  created_at = models.DateTimeField(editable=False, auto_now_add=True)
  updated_at = models.DateTimeField(editable=False, auto_now=True)
  
  def __unicode__(self):
    return u'%s' % (self.url) # TODO: REGEX videos and resize effectively, and abstact sizes to settings.py
  
class Audio(models.Model):
  PROVIDER_CHOICES = (
    ('soundcloud', 'soundcloud.com'),
  )
  embed = models.TextField(help_text="Add &lt;embed&gt;&lt;/embed&gt; code here.")
  provider = models.TextField(editable=False, max_length=10, choices=PROVIDER_CHOICES)
  content_type = models.ForeignKey(ContentType)
  object_id = models.PositiveIntegerField()
  content_object = generic.GenericForeignKey('content_type', 'object_id')
  created_at = models.DateTimeField(editable=False, auto_now_add=True)
  updated_at = models.DateTimeField(editable=False, auto_now=True)

  def __unicode__(self):
    return u'%s' % (self.embed)
    
class File(models.Model):
  path = models.FileField(upload_to="uploads/%Y/%m/%d/", max_length=255)
  content_type = models.ForeignKey(ContentType)
  object_id = models.PositiveIntegerField()
  content_object = generic.GenericForeignKey('content_type', 'object_id')
  created_at = models.DateTimeField(editable=False, auto_now_add=True)
  updated_at = models.DateTimeField(editable=False, auto_now=True)

  def __unicode__(self):
    return u'%s' % (self.path)
