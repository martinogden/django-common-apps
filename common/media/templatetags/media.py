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


class VideoEmbedNode(template.Node):
    def __init__(self, video, width, height):
        self.video, self.width, self.height = video, width, height

    def render(self, context):
        return self.video.__unicode__(self.width, self.height)


@register.tag
def embed(parser, token):
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError, \
        "embed tag takes exactly two arguments"

    try:
        width, height = bits[2].split("x")
    except ValueError:
        raise template.TemplateSyntaxError, \
        "video_embed tag must be in format {% video_tag [width]x[height] %}"


    return VideoEmbedNode(video, width, height)
