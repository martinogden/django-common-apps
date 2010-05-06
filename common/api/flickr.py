import flickr as flickr_api
from common.media.models import Image

def has_photos(model, location="local"):
  if location == "local":
    if len(model.images.filter(local_file__is_null=False)) > 0:
      return True
  else:
    if len(model.images.filter(remote_image__icontains=location)) > 0:
      return True
    else:
      return False

def add_photos(model):
  if has_photos(model, location="flickr.com") == False:
    for photos in flickr_api.photos_search(text=model.name, per_page=10):
      for photo in photos.getSizes():
        new_image = Image(url=photo['source'], thirdparty_page=photo['url'], size=photo['label'], width=photo['width'], height=photo['height'], content_object=self)
        new_image.save()