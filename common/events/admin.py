# from django.contrib import admin
# from eventsapp.events.models import *
# 
# class VenueAdmin(admin.ModelAdmin):
#   list_display = ['name', 'address', 'postcode']
#   list_filter = ['venue_type']
#   search_fields = ['name', 'address', 'postcode']
# admin.site.register(Venue, VenueAdmin)
# 
# class EventAdmin(admin.ModelAdmin):
#   list_display = ['__unicode__', 'venue', 'start_date']
#   list_filter = ['festival', 'start_date', 'venue']
#   search_fields = ['performer__name', 'venue__name', 'name']
# admin.site.register(Event, EventAdmin)
# 
# class PerformerAdmin(admin.ModelAdmin):
#   list_display = ['name', 'website', 'contact_email']
#   search_fields = ['name']
# admin.site.register(Performer, PerformerAdmin)
# 
# class ExperienceAdmin(admin.ModelAdmin):
#   list_display = ['name', 'venue', 'category']
#   list_filter = ['category']
#   search_fields = ['name', 'venue__name']
#   
# admin.site.register(Experience, ExperienceAdmin)
