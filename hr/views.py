# Create your views here.
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def index(request):
    """
    Returns homepage of majisoft
    """
    data = {}
    return render_to_response('base.html', data, context_instance=RequestContext(request))
    
def login(request):
    """
    Returns the login page
    """