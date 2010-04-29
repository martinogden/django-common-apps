from django.contrib.sites.models import Site

def shorten_url(model):
  if model.isgd is None or model.isgd == "":
    import httplib
    conn = httplib.HTTPConnection("is.gd")
    long_url = "http://%s%s" % (Site.objects.get_current().domain, model.get_permalink())
    conn.request("GET", "/api.php?longurl=%s" % (long_url))
    response = conn.getresponse()
    model.isgd = response.read()