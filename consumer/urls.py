from django.conf.urls.defaults import *
from django.conf import settings
from views import *

urlpatterns = patterns('',                       
    url(r'^view/all/$', consumer, {"action":"L"}, name='all-consumers'),
    url(r'^(?P<consumer_type>[\w-]+)/add/$', consumer, 
        {"template_name":"consumer/consumer_form.html", "action":"C"},name='consumer-add'),
    url(r'^view/(?P<pk>[\d]+)/$', consumer, {"action":"R"}, name='consumer-details'),
    url(r'^(?P<consumer_type>[\w-]+)/(?P<pk>[\d]+)/edit/$', consumer, 
        {"template_name":"consumer/consumer_form.html", "action":"U"}, name='consumer-edit'),
    url(r'^(?P<consumer_type>[\w-]+)/(?P<pk>[\d]+)/delete/$', consumer, {"action":"D"}, name='consumer-delete'),
    
)

