from django.conf.urls.defaults import *
from django.views.generic import DetailView
from consumer.models import Consumer
from django.conf import settings
from views import *

urlpatterns = patterns('',                       
    url(r'^view/all/$', consumer, {"action":"L"}, name='all-consumers'),
    url(r'^(?P<consumer_type>[\w-]+)/add/$', consumer, 
        {"template_name":"consumer/consumer_form.html", "action":"C"},name='consumer-add'),
    url(r'^view/(?P<pk>[\d]+)/$', DetailView.as_view(
            model=Consumer,
            template_name='consumer/consumer_details.html'),
        name='consumer-details'),
    url(r'^(?P<consumer_type>[\w-]+)/(?P<pk>[\d]+)/edit/$', consumer, 
        {"template_name":"consumer/consumer_form.html", "action":"U"}, name='consumer-edit'),
    url(r'^(?P<consumer_type>[\w-]+)/(?P<pk>[\d]+)/delete/$', consumer, {"action":"D"}, name='consumer-delete'),
    
)

