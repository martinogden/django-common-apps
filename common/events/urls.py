from django.conf.urls.defaults import *
import datetime
from django.views.generic import list_detail
from models import CommonEvent, CommonPerformer, CommonVenue

# Dictionaries for Generic Views
event_info = {
  "queryset": CommonEvent.objects.filter(end_date__gte=datetime.date.today()),
  "template_name": "events/list.html",
  "template_object_name": "convention",
  
}

archived_event_info = {
  "queryset": CommonEvent.objects.filter(end_date__lte=datetime.date.today()).order_by("-start_date"),
  "template_name": "events/archive_list.html",
  "template_object_name": "convention",
}

performer_info = {
  "queryset": CommonPerformer.objects.all(),
  "template_object_name": "performer",
}

# Generic Views
urlpatterns = patterns('',
  # View all upcoming / current Conventions
  url(r"^events/$", list_detail.object_list, event_info, name="upcoming_events"),
  # Archived conventions reverse date ordered
  url(r"^events/archive/$", list_detail.object_list, archived_event_info, name="events_archive"),
  # Single Event
  url(r"^event/(?P<event_id>\d{1,4})/$", list_detail.object_detail, event_info, name="event_detail"),
  
  # Performer Detail
  url(r"^performer/(?P<slug>[^/]+)/$", list_detail.object_detail, performer_info, name="performer_detail"),
)