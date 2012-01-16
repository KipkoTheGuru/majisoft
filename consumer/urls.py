from django.conf.urls.defaults import *
from django.views.generic import ListView
from consumer.models import *
from meter.models import *
from django.conf import settings
from views import *

urlpatterns = patterns('',                       
    #URLs for Consumer
    url(r'^view/$', ListView.as_view(queryset=Consumer.objects.all(), context_object_name='consumers',
                                     template_name='consumer/consumer_list.html'), name= 'consumer-list'),
    url(r'^consumer-type/$', ListView.as_view(queryset=ConsumerType.objects.all(), context_object_name='consumer_types',
                                              template_name='consumer/consumer_type.html'), name= 'consumer-type'),
    url(r'^(?P<consumer_type>[\w-]+)/add/$', consumer, {"template_name":"consumer/consumer_form.html", "action":"C"},
        name='consumer-add'),
    url(r'^view/(?P<pk>[\d]+)/$', consumer, {"template_name":"consumer/consumer_details.html", "action":"R"}, name='consumer-details'),
    url(r'^(?P<consumer_type>[\w-]+)/(?P<pk>[\d]+)/edit/$', consumer,{"template_name":"consumer/consumer_form.html", "action":"U"},
        name='consumer-edit'),
    url(r'^(?P<consumer_type>[\w-]+)/(?P<pk>[\d]+)/delete/$', consumer, {"action":"D"}, name='consumer-delete'),
    
    #URLs for Application
    url(r'^application/list/$', ListView.as_view(queryset=Application.objects.filter(reviewed=False), context_object_name='application_list',
                                     template_name='consumer/application_list.html'), name='application-list'),
    url(r'^application/rejected/list/$', ListView.as_view(queryset=Application.objects.filter(approved=False, reviewed=False), context_object_name='application_list',
                                     template_name='consumer/application_list.html'), name='rejected-list'),
    url(r'^application/(?P<consumer_pk>[\d]+)/add/$', application, {"action":"create"}, name='application-add'),
    url(r'^application/(?P<consumer_pk>[\d]+)/edit/(?P<pk>[\d]+)/$', application, {"action":"update"}, name='application-edit'),
    url(r'^application/details/(?P<pk>[\d]+)/$', application, 
        {"template_name":"consumer/application_details.html", "action":"read"}, name='application-details'),
    url(r'^application/delete/(?P<pk>[\d]+)/$', application, {"action":"delete"}, name='application-delete'),
    url(r'^application/approve/(?P<pk>[\d]+)/$', application, {"action":"approve"}, name='application-approve'),
    url(r'^application/reject/(?P<pk>[\d]+)/$', application, {"action":"reject"}, name='application-reject'),
    
    #URLs for Plots
    url(r'^plots/$', ListView.as_view(queryset=Plot.objects.all(), context_object_name='plots', template_name='consumer/plot_list.html'), 
        name= 'plot-list'),
    url(r'^plot/add/$', plot, {"action":"create"}, name='plot-add'),
    url(r'^plot/edit/(?P<pk>[\d]+)/$', plot, {"action":"update"}, name='plot-edit'),
    url(r'^plot/details/(?P<pk>[\d]+)/$', plot, {"action":"read"}, name='plot-details'),
    url(r'^plot/delete/(?P<pk>[\d]+)/$', plot, {"action":"delete"}, name='plot-delete'),
    
    #URLs for subzones, zones & regions
    url(r'^regions/$', ListView.as_view(queryset=Plot.objects.all(), context_object_name='plots', template_name='consumer/plot_list.html'), 
        name= 'plot-list'),
    url(r'^plot/add/$', plot, {"action":"create"}, name='plot-add'),
    url(r'^plot/edit/(?P<pk>[\d]+)/$', plot, {"action":"update"}, name='plot-edit'),
    url(r'^plot/details/(?P<pk>[\d]+)/$', plot, {"action":"read"}, name='plot-details'),
    url(r'^plot/delete/(?P<pk>[\d]+)/$', plot, {"action":"delete"}, name='plot-delete'),
    
    #URLs for Landlords
)


