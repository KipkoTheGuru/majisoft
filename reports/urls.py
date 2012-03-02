from django.conf.urls.defaults import *
from django.conf import settings
from views import *

urlpatterns = patterns('',
   url(r'^$', pdf_view, name='report-index'),
   url(r'^active-accounts/$', active_accounts, name='report-active-accounts'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
