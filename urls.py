from django.conf.urls.defaults import *
from django.conf import settings
from views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index, name='home'),
    url(r'^login/$', login),    
    url(r'^consumer/', include("consumer.urls")),
    url(r'^hr/', include("hr.urls")),
    url(r'^meter/', include("meter.urls")),
    url(r'^payments/', include("payments.urls")),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
         {'document_root': settings.MEDIA_ROOT}),
    )
