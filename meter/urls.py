from django.conf.urls.defaults import *
from django.views.generic import ListView
from meter.models import *
from consumer.models import *
from django.conf import settings
from views import *

urlpatterns = patterns('', 
    #URLs for Account
    url(r'^account/list/$', ListView.as_view(queryset=Account.objects.filter(closed=False), context_object_name='accounts',
                                     template_name='meter/account_list.html'), name= 'account-list'),
    url(r'^account/closed/list/$', ListView.as_view(queryset=Account.objects.filter(closed=True), context_object_name='closed_accounts',
                                     template_name='meter/account_list.html'), name= 'closed-account-list'),
    url(r'^account/application/list/$', ListView.as_view(queryset=Application.objects.filter(reviewed=False), context_object_name='applications',
                                     template_name='consumer/application_list.html'), name= 'application-list'),
    url(r'^account/application/rejected/list/$', ListView.as_view(queryset=Application.objects.filter(approved=False, reviewed=True),
                                     context_object_name='applications', template_name='meter/application_list.html'),
                                     name= 'rejected-application-list'),
    url(r'^account/add/$', account, {"action":"C"}, name='account-add'),
    url(r'^account/details/(?P<pk>[\d]+)/$', account, {"action":"R", "template_name":"consumer/account_details.html"}, name='account-details'),
    url(r'^account/edit/(?P<pk>[\d]+)/$', account, {"action":"U"}, name='account-edit'),
    url(r'^account/activate/(?P<pk>[\d]+)/$', account, {"action":"activate"}, name='account-activate'),
    url(r'^account/close/(?P<pk>[\d]+)/$', account, {"action":"close"}, name='account-close'),
    
    #URLs for Subzones
    url(r'^subzone/list/$', ListView.as_view(queryset=SubZone.objects.all(), context_object_name='subzones',
                                     template_name='meter/subzone_list.html'), name= 'subzone-list'),
    url(r'^subzone/add/$', subzone, {"action":"C"}, name='subzone-add'),
    url(r'^subzone/add/(?P<zone_pk>[\d]+)/$', subzone, {"action":"C"}, name='subzone-zone-add'),
    url(r'^subzone/details/(?P<pk>[\d]+)/$', subzone, {"action":"R", "template_name":"meter/subzone_details.html"}, name='subzone-details'),
    url(r'^subzone/edit/(?P<pk>[\d]+)/$', subzone, {"action":"U"}, name='subzone-edit'),
    url(r'^subzone/delete/(?P<pk>[\d]+)/$', subzone, {"action":"D"}, name='subzone-delete'),
    
    #URLs for Zones
    url(r'^zone/list/$', ListView.as_view(queryset=Zone.objects.all(), context_object_name='zones',
                                     template_name='meter/zone_list.html'), name= 'zone-list'),
    url(r'^zone/add/$', zone, {"action":"C"}, name='zone-add'),
    url(r'^zone/add/(?P<region_pk>[\d]+)/$', zone, {"action":"C"}, name='zone-region-add'),
    url(r'^zone/details/(?P<pk>[\d]+)/$', zone, {"action":"R", "template_name":"meter/zone_details.html"}, name='zone-details'),
    url(r'^zone/edit/(?P<pk>[\d]+)/$', zone, {"action":"U"}, name='zone-edit'),
    url(r'^zone/delete/(?P<pk>[\d]+)/$', zone, {"action":"D"}, name='zone-delete'),
    
    #URLs for Regions
    url(r'^region/list/$', ListView.as_view(queryset=Region.objects.all(), context_object_name='regions',
                                     template_name='meter/region_list.html'), name= 'region-list'),
    url(r'^region/add/$', region, {"action":"C"}, name='region-add'),
    url(r'^region/details/(?P<pk>[\d]+)/$', region, {"action":"R", "template_name":"meter/region_details.html"}, name='region-details'),
    url(r'^region/edit/(?P<pk>[\d]+)/$', region, {"action":"U"}, name='region-edit'),
    url(r'^region/delete/(?P<pk>[\d]+)/$', region, {"action":"D"}, name='region-delete'),
)

