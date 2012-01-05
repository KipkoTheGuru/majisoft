# Create your views here.
from consumer.models import Consumer
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from consumer.forms import ConsumerForm
from django.http import HttpResponseForbidden

def consumer(request, pk=None, action=None, template_name="consumer/consumer_details.html"):
    data = {}
    if request.method == "GET":
        if action == "R":
            if pk:
                consumer = get_object_or_404(Consumer, pk=pk)
                data['consumer'] = consumer
        else:
            return HttpResponseForbidden()
    elif request.method == "POST":
        if action in ("C","D","U"):
            if action in ("C","U"):
                if pk:
                    consumerForm = ConsumerForm(request.POST, instance=get_object_or_404(Consumer, pk=pk))
                else:
                    consumerForm = ConsumerForm(request.POST)
        
                if consumerForm.is_valid():
                    consumer = consumerForm.save()
            else:
                consumer = get_object_or_404(Consumer, pk=pk)
                consumer.delete()
        else:
            return HttpResponseForbidden()
    return render_to_response(template_name, data, context_instance=RequestContext(request))
    