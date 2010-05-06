import pylast
from django.conf import settings
class Lastfm:
  def __init__(self, performer):
    try:
      API_KEY = settings.LASTFM_API_KEY
      API_SECRET = settings.LASTFM_API_SECRET
      username = settings.LASTFM_USERNAME
      password = settings.LASTFM_PASSWORD
    except AttributeError:
      API_KEY = "724bf07f27e43443f07875f3148c28e7"
      API_SECRET = "f9d0024a7c7c68fe252c6a1376dc7959"
      username = "wearecahoona"
      password = "m0tivation"
      
    password_hash = pylast.md5(password)
    network = pylast.get_lastfm_network(api_key = API_KEY, api_secret = API_SECRET, username = username, password_hash = password_hash)

    # Artist / Performer Model instance
    self.performer = performer
    # Lastfm artist
    self.artist = network.get_artist(self.performer.name)
    
  def _has_photos(self, location="local"):
    if location == "local":
      if len(self.performer.images.filter(local_file__is_null=False)) > 0:
        return True
    else:
      if len(self.performer.images.filter(remote_image__icontains=location)) > 0:
        return True
      else:
        return False
        
  def artist_meta(self):  
    # Description
    from httplib import BadStatusLine
    if self.performer.lastfm_description is None or len(self.performer.lastfm_description) < 1:
      try:
        self.performer.lastfm_description = self.artist.get_bio_summary()
      except pylast.WSError:
        pass
      except BadStatusLine:
        pass
    # Url
    if self.performer.lastfm_link is None:
      try:
        self.performer.lastfm_link = self.artist.get_url()
      except pylast.WSError:
        pass
      except BadStatusLine:
        pass
        
  def add_photos(self):
    if self._has_photos("last.fm") == False:
      # Add Last.fm Images
      try:
        i = artist.get_images(limit=1)
        try:
          # Add 10 images in all sizes available
          for image in i:
            sizes = []
            for size in image['sizes']:
              sizes.append(size)
            for size in sizes:
              new_image = Image(url=image['sizes'][size], thirdparty_page=image['url'], size=size, content_object=self)
              new_image.save()
        except IndexError:
          pass
      except BadStatusLine:
        pass
      except pylast.WSError:
        pass
        
  def add_tags(self):
    # Add Last.fm Tags
    lastfm_tags = []
    try:
      lastfm_tags = self.artist.get_top_tags()
    except WSError:
      pass
    from django.core.exceptions import ObjectDoesNotExist
    for tag in lastfm_tags:
      if int(tag['weight']) > 5:
        try:
          Tag.objects.get(name=tag['item'])
        except ObjectDoesNotExist:
          t =Tag(name=tag['item'], weight=tag['weight'])
          t.save()
        add_tag = Tag.objects.get(name=tag['item'])
        self.tags.add(add_tag)