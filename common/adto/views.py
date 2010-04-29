from common.adto.models  import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

def display_banner(request, banner_id):
  banner_id = int(banner_id)
  banner = get_object_or_404(Banner, pk=banner_id)
  return HttpResponse("%s" % banner)
  
def redirect(request, banner_id):
  banner_id = int(banner_id)
  banner = get_object_or_404(Banner, pk=banner_id)
  banner.click()
  banner.save()
  
  from exceptions import KeyError
  try:
    referrer = request.META['HTTP_REFERER']
  except KeyError:
    referrer = "Direct Link"
    
  if banner_id == 4:
    
    # Virgin Add Hack
    if referrer == "Direct Link":
      redir_url = banner.href
    else:
      section = referrer.split("/")[3]
      
      try:
        # Cheeky switch
        redir_url = {
          'experiences': "http://ad-emea.doubleclick.net/click;h=v2|3C40|0|0|%2a|g;223288591;0-0;0;47037043;31-1|1;35976533|35994411|1;;%3fhttp://www.farefinder.virgintrains.co.uk/",
          'transport': "http://ad-emea.doubleclick.net/click;h=v2|3C40|0|0|%2a|a;223288591;0-0;0;47037046;31-1|1;35976533|35994411|1;;%3fhttp://www.farefinder.virgintrains.co.uk/",
          'events': "http://ad-emea.doubleclick.net/click;h=v2|3C40|0|0|%2a|e;223288591;0-0;0;47037044;31-1|1;35976533|35994411|1;;%3fhttp://www.farefinder.virgintrains.co.uk/",
          'event': "http://ad-emea.doubleclick.net/click;h=v2|3C40|0|0|%2a|e;223288591;0-0;0;47037044;31-1|1;35976533|35994411|1;;%3fhttp://www.farefinder.virgintrains.co.uk/",
          'accommodation': "http://ad-emea.doubleclick.net/click;h=v2|3C40|0|0|%2a|c;223288591;0-0;0;47037045;31-1|1;35976533|35994411|1;;%3fhttp://www.farefinder.virgintrains.co.uk/",
        }[section]
      except KeyError:
        redir_url = "http://ad-emea.doubleclick.net/click;h=v2|3C40|0|0|%2a|m;223288591;0-0;0;47037040;31-1|1;35976533|35994411|1;;%3fhttp://www.farefinder.virgintrains.co.uk/"
  else:
    # Not virgin ad
    redir_url = banner.href
    
  r = Referrer(href = referrer, banner = banner)
  r.save()
  
  return HttpResponseRedirect(redir_url)