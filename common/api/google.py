from django.conf import settings

def geolocate(location):
  try:
    api_key = settings.GOOGLE_MAPS_API_KEY
  except AttributeError:
    api_key = "ABQIAAAAzMUFFnT9uH0xq39J0Y4kbhTJQa0g3IQ9GZqIMmInSLzwtGDKaBR6j135zrztfTGVOm2QlWnkaidDIQ"
    
  if location.latitude is None or location.latitude == 0:
    from geopy import geocoders
    g = geocoders.Google(api_key ,domain='maps.google.co.uk', resource='maps')
  
    #is actually just postcode
    full_address = "%s, UK" % (location.postcode)
    # Allow for place not found error
    lat = None
    from exceptions import ValueError
    try:
      geocode = g.geocode(full_address)
      place, (lat, lng) = geocode
    except ValueError:
      # Alternate lookup: Try search with just business and and "Manchester, UK"
      try:
        name_and_city = "%s, %s, UK" % (location.name, location.city)
        geocode = g.geocode(name_and_city)
        place, (lat, lng) = geocode
      except ValueError:
        pass
      pass
    if lat is not None:
      location.latitude = lat
      location.longitude = lng