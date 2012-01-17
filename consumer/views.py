# Create your views here.
from consumer.models import *
from meter.models import Account
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from consumer.forms import *
from django.http import *
from django.core.urlresolvers import reverse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

def account_set(applications, active=True, closed=False):
    accounts = []
    for application in [application_set for application_set in applications.filter(account__is_active=active, account__closed=closed)]:
        accounts.extend(list(application.account_set.all()))
    return accounts

def consumer(request, pk=None, action=None, consumer_type='domestic', template_name="consumer/consumer_details.html"):
    data = {}
    ConsumerForm = DomesticConsumerForm if consumer_type.lower() == 'domestic' else CorporateConsumerForm
    
    if request.method == "GET":
        if action in ("C", "R", "U"):
            if pk:
                consumer = get_object_or_404(Consumer, pk=pk)
                data['consumer'] = consumer
                data['consumer_type'] = consumer_type
                data['applications'] = consumer.application_set.all()
                data['unreviewed_applications'] = consumer.application_set.filter(reviewed=False)
                data['active_accounts'] = account_set(data['applications'])
                data['inactive_accounts'] = account_set(data['applications'], active=False)
                data['suspended_accounts'] = account_set(data['applications'], active=False, closed=True)
                if action in "U":
                    data["consumerForm"] = ConsumerForm(instance=get_object_or_404(Consumer, pk=pk))
            else:
                data['consumer_type'] = consumer_type
                data["consumerForm"] = ConsumerForm()
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
                    consumer = consumerForm.save(commit=False)
                    consumer.consumer_type = get_object_or_404(ConsumerType, consumer_type__iexact=consumer_type)
                    consumer.save()
                    return HttpResponseRedirect(reverse("application-add", args=[consumer.pk]) if action=="C" else consumer.get_absolute_url())
                else:
                    consumerForm = ConsumerForm(request.POST, instance=get_object_or_404(Consumer, pk=pk))
            else:
                consumer = get_object_or_404(Consumer, pk=pk)
                consumer.delete()
        else:
            return HttpResponseForbidden()
    return render_to_response(template_name, data, context_instance=RequestContext(request))

@csrf_exempt
def application(request, consumer_pk=None, pk=None, action=None, template_name="consumer/consumer_application.html"):
    data = {}
    if request.method == "GET":
        if action in ("create", "read", "update"):
            if pk:
                data['application'] = get_object_or_404(Application, pk=pk)
                if action == "update":
                    data['applicationForm'] = ApplicationForm()
            else:
                data['applicant'] = get_object_or_404(Consumer, pk=consumer_pk)
                data['applicationForm'] = ApplicationForm()
        else:
            return HttpResponseForbidden()
    elif request.method == "POST":
        if action in ("create","delete","update"):
            if pk:
                applicationForm = ApplicationForm(request.POST, instance=get_object_or_404(Application, pk=pk))
            else:
                applicationForm = ApplicationForm(request.POST)
            if applicationForm.is_valid():
                application = applicationForm.save(commit=False)
                application.consumer = get_object_or_404(Consumer, id=consumer_pk)
                application.save()
                return HttpResponseRedirect(application.consumer.get_absolute_url())
        elif action in ("approve", "reject"):
            application = get_object_or_404(Application, pk=pk)
            application.reviewed = True
            if action == "approve":
                application.approved = True
                account = Account(application=application)
                account.save()
            else:
                application.approved = False
            application.save()
            return HttpResponseRedirect(application.consumer.get_absolute_url())
    return render_to_response(template_name, data, context_instance=RequestContext(request))

def plot(request, pk=None, landlord_id=None, action=None, template_name="consumer/plot_form.html"):
    data = {}
    if request.method == "GET":
        if action in ("create", "read", "update"):
            if pk:
                data['plot'] = get_object_or_404(Plot, pk=pk)
                data['accounts'] = account_set(data['plot'].application_set.filter(reviewed=True, approved=True))
                if action == "update":
                    data['plotForm'] = PlotForm(instance=get_object_or_404(Plot, pk=pk))
            else:
                data['plotForm'] = PlotForm()
                data['landlord'] = get_object_or_404(Landlord, pk=landlord_id)
                if not landlord_id:
                    data['landlordForm'] = LandlordForm()
    elif request.method == "POST":
        if action in ("create", "read", "update"):
            if pk:
                plotForm = PlotForm(request.POST, instance=get_object_or_404(Plot, pk=pk))
            else:
                plotForm = PlotForm(request.POST)
                if not landlord_id:
                    landlordForm = LandlordForm(request.POST)
            if plotForm.is_valid():
                plot = plotForm.save(commit=False)
                if not landlord_id:
                    if landlordForm.is_valid():
                        landlord = landlordForm.save()
                        plot.landlord = landlord
                    else:
                        data['landlordForm'] = LandlordForm()
                else:
                    plot.landlord = get_object_or_404(Landlord, pk=landlord_id)
                plot.save()
                return HttpResponseRedirect(plot.landlord.get_absolute_url())
    return render_to_response(template_name, data, context_instance=RequestContext(request))

def landlord (request, pk=None, action=None, template_name="consumer/landlord_form.html"):
    data = {}
    if request.method == "GET":
        if action in ("create", "read", "update"):
            if pk:
                data['landlord'] = get_object_or_404(Landlord, pk=pk)
                if action == "update":
                    data['landlordForm'] = LandlordForm()
            else:
                data['plotForm'] = PlotForm()
    elif request.method == "POST":
        pass
    return render_to_response(template_name, data, context_instance=RequestContext(request))