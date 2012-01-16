from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView
from django.conf import settings
from views import *
from consumer.models import Application
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(queryset=Application.objects.filter(approved=False), context_object_name='latest_applications',
                                template_name='home.html'), name='home'),
    url(r'^login/$', login, name='login'),    
    url(r'^consumer/', include('consumer.urls')),
    url(r'^meter/', include('meter.urls')),
    url(r'^hr/', include('hr.urls')),
    url(r'^finance/', include('payments.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
         {'document_root': settings.MEDIA_ROOT}),
    )
