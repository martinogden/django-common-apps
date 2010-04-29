from django.contrib import admin
from common.adto.models import Banner

class BannerAdmin(admin.ModelAdmin):
  list_display = ['name', 'impressions', 'clicks']
  list_filter = ['name']
  
admin.site.register(Banner, BannerAdmin)