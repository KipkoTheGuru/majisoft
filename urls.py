from django.conf.urls.defaults import *
from django.views.generic import ListView
from django.conf import settings
from views import *
from consumer.models import Application
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
   url(r'^$', index, name='index'),
   url(r'^core/', include("consumer.urls")),
   url(r'^payments/', include("payments.urls")),
   url(r'^hr/', include("hr.urls")),
   url(r'^meter/', include("meter.urls")),
   url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('',
    url(r'^dashboard/$', ListView.as_view(queryset=Application.objects.filter(reviewed=False), context_object_name='latest_applications',
                      template_name='home.html'), name='home'),
    url(r'^login/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', logout, name='logout'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
