from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from consumer.models import Consumer

def index(request):
    """
    Returns homepage of majisoft
    """
    new_customers = Consumer.objects.all()
    
    data = {"new_customers":new_customers}
    return render_to_response('home.html', data, context_instance=RequestContext(request))

def login(request, template_name="login.html"):
    user = User.objects.get(username=request.POST['username'])
    if user.password == request.POST['password']:
        request.session['member_id'] = user.id
        request.session['user_type'] = user.username
        request.session['name'] = user.consumer_set.filter(id=user.id).first_name
        return HttpResponseRedirect(reverse("home"))