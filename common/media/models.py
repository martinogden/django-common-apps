from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.safestring import SafeUnicode

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
      return SafeUnicode('%s' % (self.local_image.name))
    else:
      return SafeUnicode('%s' % (self.remote_image))
      
class Video(models.Model):
  PROVIDER_CHOICES = (
    ('youtube', 'youtube.com'),
    ('vimeo', 'vimeo.com'),
  )
  url = models.URLField(max_length=255, help_text="Copy the url from te address bar for the Vimeo or youtube video. Do NOT copy the ambed code.")
  provider = models.TextField(max_length=10, choices=PROVIDER_CHOICES, editable=False)
  content_type = models.ForeignKey(ContentType)
  object_id = models.PositiveIntegerField()
  content_object = generic.GenericForeignKey('content_type', 'object_id')
  created_at = models.DateTimeField(editable=False, auto_now_add=True)
  updated_at = models.DateTimeField(editable=False, auto_now=True)
  
  def clean(self):
    # Only allow for Youtube or Vimeo
    if self.url.find("youtube.com") is -1 and self.url.find("vimeo.com") is -1:
      raise ValidationError(u'Video must be from either Vimeo or Youtube')
      
  def save(self):
    # Decide which provider video is from:
    if self.url.find("youtube.com"):
      self.provider = "youtube.com"
    elif self.url.find("vimeo.com"):
      self.provider = "vimeo.com"
      
    super(Video, self).save()
    
  def __unicode__(self):
    if self.provider == "vimeo.com":
      video_id = self.url.split("/")[-1]
      return SafeUnicode('<object width="%s" height="%s"><param name="allowfullscreen" value="true" /><param name="allowscriptaccess" value="always" /><param name="movie" value="http://vimeo.com/moogaloop.swf?clip_id=%s&amp;server=vimeo.com&amp;show_title=1&amp;show_byline=1&amp;show_portrait=0&amp;color=&amp;fullscreen=1" /><embed src="http://vimeo.com/moogaloop.swf?clip_id=%s&amp;server=vimeo.com&amp;show_title=1&amp;show_byline=1&amp;show_portrait=0&amp;color=&amp;fullscreen=1" type="application/x-shockwave-flash" allowfullscreen="true" allowscriptaccess="always" width="%s" height="%s"></embed></object>' % (settings.VIDEO_WIDTH, settings.VIDEO_HEIGHT, video_id, video_id, settings.VIDEO_WIDTH, settings.VIDEO_HEIGHT))
    elif self.provider == "youtube.com":
      video_id = self.url.split("v=")[-1]
      return SafeUnicode('<object width="%s" height="%s"><param name="movie" value="http://www.youtube.com/v/%s&hl=en_US&fs=1&"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="http://www.youtube.com/v/%s&hl=en_US&fs=1&" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="%s" height="%s"></embed></object>' % (settings.VIDEO_WIDTH, settings.VIDEO_HEIGHT, video_id, video_id, settings.VIDEO_WIDTH, settings.VIDEO_HEIGHT))
      
class Audio(models.Model):
  PROVIDER_CHOICES = (
    ('soundcloud', 'soundcloud.com'),
  )
  link = models.URLField(help_text="Add link here, NOT embed code.", max_length=255)
  provider = models.TextField(editable=False, max_length=10, choices=PROVIDER_CHOICES)
  content_type = models.ForeignKey(ContentType)
  object_id = models.PositiveIntegerField()
  content_object = generic.GenericForeignKey('content_type', 'object_id')
  created_at = models.DateTimeField(editable=False, auto_now_add=True)
  updated_at = models.DateTimeField(editable=False, auto_now=True)
  
  class Meta:
    verbose_name_plural = "Audio"
  def clean(self):
    # Only allow for Youtube or Vimeo
    if self.url.find("soundcloud.com") is -1:
      raise ValidationError(u'Audio must be from Soundcloud')
      
  def save(self):
    if self.url.find("soundcloud.com"):
      self.provider = "soundcloud.com"
    super(Audio. self).save()
    
  def __unicode__(self):
    if self.provider == "soundcloud.com":
      return SafeUnicode('<object width="%s" height="%s"><param name="movie" value="http://player.soundcloud.com/player.swf?url=%s&&color=0066cc"></param><param name="allowscriptaccess" value="always"></param><embed allowscriptaccess="always" src="http://player.soundcloud.com/player.swf?url=%s&&color=0066cc" type="application/x-shockwave-flash" width="%s" height="%s"></embed></object>' % (settings.SOUNDCLOUD_WIDTH, settings.SOUNDCLOUD_HEIGHT, self.url, self.url, settings.SOUNDCLOUD_WIDTH, settings.SOUNDCLOUD_HEIGHT))
    
class File(models.Model):
  path = models.FileField(upload_to="uploads/%Y/%m/%d/", max_length=255)
  content_type = models.ForeignKey(ContentType)
  object_id = models.PositiveIntegerField()
  content_object = generic.GenericForeignKey('content_type', 'object_id')
  created_at = models.DateTimeField(editable=False, auto_now_add=True)
  updated_at = models.DateTimeField(editable=False, auto_now=True)

  def __unicode__(self):
    return u'%s' % (self.path)
