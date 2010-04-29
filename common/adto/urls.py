from django.conf.urls.defaults import *


urlpatterns = patterns('common.adto.views',
  (r'^affiliate/(?P<banner_id>\d{1,2})/$', 'redirect'),
)