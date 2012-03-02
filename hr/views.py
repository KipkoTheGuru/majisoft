from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from models import Employee

def profile(request, action=None, template_name=None):
    data={}
    if request.method == "GET":
        if action == "R":
            data['user_details'] = get_object_or_404 (Employee, user = request.user)
    return render_to_response(template_name, data, context_instance=RequestContext(request))