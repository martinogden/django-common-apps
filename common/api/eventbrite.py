from django.conf import settings

"""
Eventbrite api
Eventbrite wouldnt import from site packages... wierd.
"""

__author__    = "Josh Toft <josh@fwix.com>"
__copyright__ = "Copyright 2010 Fwix, Inc."
__license__   = "MIT"

from hashlib import md5
import urllib

import httplib2
import simplejson

__all__ = ['APIError', 'API']

class APIError(Exception):
    pass

class API:
    def __init__(self, app_key, server='www.eventbrite.com', cache=None):
        """Create a new Eventbrite API client instance.
        If you don't have an application key, you can request one:
        http://www.eventbrite.com/api/key/"""
        self.app_key = app_key
        self.server = server
        self.http = httplib2.Http(cache)

    def call(self, method, **args):
        "Call the Eventbrite API's METHOD with ARGS."
        # Build up the request
        args['app_key'] = self.app_key
        if hasattr(self, 'user_key'):
            args['user'] = self.user
            args['user_key'] = self.user_key
        args = urllib.urlencode(args)
        url = "http://%s/json/%s?%s" % (self.server, method, args)

        # Make the request
        response, content = self.http.request(url, "GET")

        # Handle the response
        status = int(response['status'])
        if status == 200:
            try:
                return simplejson.loads(content)
            except ValueError:
                raise APIError("Unable to parse API response!")
        elif status == 404:
            raise APIError("Method not found: %s" % method)
        else:
            raise APIError("Non-200 HTTP response status: %s" % response['status'])

def new(event):
  try:
    api_key = settings.EVENTBRITE_API_KEY
    user_key = settings.EVENTBRITE_USER_KEY
  except AttributeError:
    api_key = "MWIyZTZmY2Q0MDRl"
    user_key="12597698692846443790"
    
  from django.template.defaultfilters import slugify
  eb = API(api_key)
  add_event = eb.call(
    method="event_new", 
    user_key=user_key,                      # Link Event to My UID (API User Key)
    title=event.__unicode__(),
    description=event.description,
    start_date="%s 00:00:00" % str(event.start_date),      # TODO: Might need to work on this to add time
    end_date="%s 23:59:59" % str(event.end_date),          # TODO: Might need to work on this to add time
    timezone="GMT+00",                                    # TODO: Find which timezone event is in
    personalized_url=slugify(event.__unicode__()),
    status="live",
  )
  
  from exceptions import KeyError
  try:
    add_event['error']
    return add_event['error']
  except KeyError:
    get_event = eb.call(
      method = "event_get",
      id = add_event['process']['id']
    )
    event.eventbrite_link = get_event['event']['url']