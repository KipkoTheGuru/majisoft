from django.conf.urls.defaults import *
from django.views.generic import ListView
from consumer.models import Application
from django.conf import settings
from views import *
from django.contrib.auth.views import password_change

urlpatterns = patterns('',
    url(r'^profile/$', profile, {"action":"R", "template_name":"hr/profile_details.html"}, name='profile-details'),
    url(r'^change-password/$', password_change, {'template_name': 'hr/profile_change_pass.html','post_change_redirect': '/my-account/profile/'}, name='profile-change-pass'),
)