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
  
  def save(self, *args, **kwargs):
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

    super(Image, self).save(*args, **kwargs)
  
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
      
  def save(self, *args, **kwargs):
    # Decide which provider video is from:
    if self.url.find("youtube.com") > 0:
      self.provider = "youtube.com"
    if self.url.find("vimeo.com") > 0:
      self.provider = "vimeo.com"
      
    super(Video, self).save(*args, **kwargs)
    
  def __unicode__(self, width=False, height=False):
    if not width:
      width = settings.VIDEO_WIDTH
    if not height:
      height = settings.VIDEO_HEIGHT
      
    if self.provider == "vimeo.com":
      video_id = self.url.split("/")[-1]
      return SafeUnicode('<object width="%s" height="%s"><param name="allowfullscreen" value="true" /><param name="allowscriptaccess" value="always" /><param name="movie" value="http://vimeo.com/moogaloop.swf?clip_id=%s&amp;server=vimeo.com&amp;show_title=1&amp;show_byline=1&amp;show_portrait=0&amp;color=&amp;fullscreen=1" /><embed src="http://vimeo.com/moogaloop.swf?clip_id=%s&amp;server=vimeo.com&amp;show_title=1&amp;show_byline=1&amp;show_portrait=0&amp;color=&amp;fullscreen=1" type="application/x-shockwave-flash" allowfullscreen="true" allowscriptaccess="always" width="%s" height="%s"></embed></object>' % (width, height, video_id, video_id, width, height))
    elif self.provider == "youtube.com":
      video_id = self.url.split("v=")[-1]
      return SafeUnicode('<object width="%s" height="%s"><param name="movie" value="http://www.youtube.com/v/%s&hl=en_US&fs=1&"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="http://www.youtube.com/v/%s&hl=en_US&fs=1&" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="%s" height="%s"></embed></object>' % (width, height, video_id, video_id, width, height))

  # returns a thumbnail for the video  
  def get_thumbnail(self):
      if self.provider == "vimeo.com":
          try:
              import urllib2
              from xml.dom import minidom
              # get thumbnail using api (need to set user agent as vimeo's api doesn't like urllib for some reason)
              video_id = self.url.split("/")[-1]
              handle = urllib2.build_opener()
              request = urllib2.Request("http://vimeo.com/api/v2/video/%s.xml" % (video_id))
              request.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7 GTB6 (.NET CLR 3.5.30729)")
              data = minidom.parseString(handle.open(request).read())
              thumbnail = data.getElementsByTagName("thumbnail_large")[0].firstChild.nodeValue
              return thumbnail
          except:
              return ""
      elif self.provider == "youtube.com":
          # get thumbnail via http
          video_id = self.url.split("v=")[-1]
          return "http://img.youtube.com/vi/%s/0.jpg" % video_id
      
class Audio(models.Model):
  PROVIDER_CHOICES = (
    ('soundcloud', 'soundcloud.com'),
  )
  embed = models.URLField(help_text="Add link here, NOT embed code.", max_length=255, verbose_name="Audio URL")
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
    if self.embed.find("soundcloud.com") is -1:
      raise ValidationError(u'Audio must be from Soundcloud')
      
  def save(self, *args, **kwargs):
    if self.embed.find("soundcloud.com"):
      self.provider = "soundcloud.com"
    super(Audio, self).save(*args, **kwargs)
    
  def __unicode__(self):
    if self.provider == "soundcloud.com":
      # Seems links are quite hard to extract from soundcloud share button etc.
      # return SafeUnicode('<object width="%s" height="%s"><param name="movie" value="http://player.soundcloud.com/player.swf?url=%s&&color=0066cc"></param><param name="allowscriptaccess" value="always"></param><embed allowscriptaccess="always" src="http://player.soundcloud.com/player.swf?url=%s&&color=0066cc" type="application/x-shockwave-flash" width="%s" height="%s"></embed></object>' % (settings.SOUNDCLOUD_WIDTH, settings.SOUNDCLOUD_HEIGHT, self.url, self.url, settings.SOUNDCLOUD_WIDTH, settings.SOUNDCLOUD_HEIGHT))
      return SafeUnicode(self.embed)

     
  @property 
  def video_id(self):
    if self.provider == "vimeo.com":
      return self.url.split("/")[-1]
    elif self.provider == "youtube.com":
      return self.url.split("v=")[-1]

      
class File(models.Model):
  path = models.FileField(upload_to="uploads/%Y/%m/%d/", max_length=255)
  content_type = models.ForeignKey(ContentType)
  object_id = models.PositiveIntegerField()
  content_object = generic.GenericForeignKey('content_type', 'object_id')
  created_at = models.DateTimeField(editable=False, auto_now_add=True)
  updated_at = models.DateTimeField(editable=False, auto_now=True)

  def __unicode__(self):
    return u'%s' % (self.path)
