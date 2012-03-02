from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.views import login as auth_login, logout_then_login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from consumer.models import Consumer
from django.contrib.auth.forms import AuthenticationForm
from hr.helper import checkCredentials, checkReceptionist


@login_required
def index(request):
    if checkReceptionist(request):
        return HttpResponseRedirect(reverse("consumer-list"))
    if checkCredentials(request):
        return HttpResponseRedirect(reverse('meter-readings-add'))
    return HttpResponseRedirect(reverse('home'))

def login(request, *args, **kwargs):
    if not request.user.is_authenticated():
        return auth_login(request, *args, **kwargs)
    else:
        if checkCredentials(request):
            return HttpResponseRedirect(reverse('meter-readings-add'))
        return HttpResponseRedirect(reverse('home'))

def logout(request, *args, **kwargs):
    if request.user.is_authenticated():
        return logout_then_login(request, *args, **kwargs)
    else:
        return HttpResponseRedirect(reverse('login'))