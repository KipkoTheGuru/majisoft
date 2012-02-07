from django.conf.urls.defaults import *
from django.views.generic import ListView
from payments.models import *
from django.conf import settings
from views import *

urlpatterns = patterns('',
    ##URLs for Fee and Charge Types
    url(r'^fees-charges/list/$', ListView.as_view(queryset=Fee.objects.all(), context_object_name='fees',
                                              template_name='payments/fee_list.html'), name= 'fee-list'),
    url(r'^fees-charges/add/$', fee, {"action":"create"}, name='fee-add'),
    url(r'^fees-charges/details/(?P<pk>[\d]+)/$', fee, {"action":"read", "template_name":"payments/fee_details.html"}, name='fee-details'),
    url(r'^fees-charges/edit/(?P<pk>[\d]+)/$', fee, {"action":"update"}, name='fee-edit'),
    url(r'^fees-charges/delete/(?P<pk>[\d]+)/$', fee, {"action":"delete"}, name='fee-delete'),
    
    #URLs for PaymentModes
    url(r'^payment-mode/list/$', ListView.as_view(queryset=PaymentMode.objects.all(), context_object_name='payment_modes',
                                              template_name='payments/payment_mode_list.html'), name= 'payment-mode-list'),
    url(r'^payment-mode/add/$', payment_mode, {"action":"create"}, name='payment-mode-add'),
    url(r'^payment-mode/details/(?P<pk>[\d]+)/$', payment_mode, {"action":"read", "template_name":"payments/payment_mode_details.html"}, name='payment-mode-details'),
    url(r'^payment-mode/edit/(?P<pk>[\d]+)/$', payment_mode, {"action":"update"}, name='payment-mode-edit'),
    url(r'^payment-mode/delete/(?P<pk>[\d]+)/$', payment_mode, {"action":"delete"}, name='payment-mode-delete'),
    
    #URLs for Payments
    url(r'^payment/(?P<pk>[\d]+)/$', payment, {"action":"create"}, name='payment-make'),
    """url(r'^payment-mode/details/(?P<pk>[\d]+)/$', payment_mode, {"action":"read", "template_name":"payments/payment_mode_details.html"}, name='payment-mode-details'),
    url(r'^payment-mode/edit/(?P<pk>[\d]+)/$', payment_mode, {"action":"update"}, name='payment-mode-edit'),
    url(r'^payment-mode/delete/(?P<pk>[\d]+)/$', payment_mode, {"action":"delete"}, name='payment-mode-delete'),"""
)