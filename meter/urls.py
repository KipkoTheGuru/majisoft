from django.conf.urls.defaults import *
from django.views.generic import ListView
from meter.models import Account
from consumer.models import Application
from django.conf import settings
from views import *

urlpatterns = patterns('', 
    #URLs for Account
    url(r'^account/list/$', ListView.as_view(queryset=Account.objects.filter(closed=False), context_object_name='accounts',
                                     template_name='meter/account_list.html'), name= 'account-list'),
    url(r'^account/closed/list/$', ListView.as_view(queryset=Account.objects.filter(closed=True), context_object_name='accounts',
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
)

