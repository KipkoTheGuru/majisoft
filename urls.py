from django.conf.urls.defaults import *
from django.conf import settings
from hr import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$',views.login)
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
         {'document_root': settings.MEDIA_ROOT}),
    )
