from django import template
register = template.Library()
from common.media.models import Video

@register.simple_tag
def video(pk, width, height):
  try:
    video = Video.objects.get(pk=pk)
  except Video.DoesNotExist:
    return False
    
  if width and height:
    width = int(width)
    height = int(height)
    return video.__unicode__(width, height)
  else:
    return video