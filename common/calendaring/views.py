from django.views.generic.simple import direct_to_template

def get_site():
  from django.contrib.sites.models import Site
  return Site.objects.get_current()
  
def ical(request, queryset, filename="calendar"):
  context = {"site": get_site()}
  # Decide whether event is singular or a list
  try:
    is_list = queryset[0]
    context["events"] = queryset
  except TypeError:
    context["events"] = [queryset]

  response = direct_to_template(request, "calendar/ical.ics", context, mimetype = "text/calendar")
  response["Content-Disposition"] = "attachment; filename=%s.ics" % (filename)
  return response
  
def google(event):
  from django.template import Template, Context
  context = {"event": event, "site": get_site()}
  url_string = "http://www.google.com/calendar/event?action=TEMPLATE&text={{ event|urlencode }}&dates={{ event.start_date|date:'Ymd\THis\Z' }}/{{ event.end_date|date:'Ymd\THis\Z' }}&details={{ event.description|safe|escape|striptags|urlencode }}&location={{ event.venue.name|urlencode }}%2C%20{{ event.venue.address|escape|linebreaks|striptags|urlencode }}%2C%20{{ event.venue.city|urlencode }}&trp=false&sprop=http://{{ site.domain }}{{ event.get_permalink }}&sprop=name:{{ site.domain }}"
  t = Template(url_string)
  c = Context(context)
  return t.render(c)
  
def yahoo(event):
  from django.template import Template, Context
  context = {"event": event, "site": get_site()}
  
  duration = (event.end_date - event.end_date).seconds*3600
  if duration == 0:
    duration = "0400"
  url_string = "http://calendar.yahoo.com/?v=60&DUR=0400&TITLE={{ event|urlencode }}&ST={{ event.start_date|date:'Ymd\THis' }}&in_loc={{ event.venue.name|urlencode }}%2C%20{{ event.venue.address|escape|linebreaks|striptags|urlencode }}%2C%20{{ event.venue.city|urlencode }}&DESC={{ event.description|safe|escape|striptags|urlencode }}&URL=http://{{ site.domain }}{{ event.get_permalink }}"
  t = Template(url_string)
  c = Context(context)
  return t.render(c)