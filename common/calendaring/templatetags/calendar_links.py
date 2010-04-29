from django import template
register = template.Library()
from django.utils.safestring import mark_safe

@register.filter
def google_calendar(event):
  from calendaring.views import google
  return mark_safe(google(event))
  
@register.filter
def yahoo_calendar(event):
  from calendaring.views import yahoo
  return mark_safe(yahoo(event))