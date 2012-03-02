# Create your views here.
from consumer.models import *
from meter.models import Account
from django.shortcuts import get_object_or_404, render_to_response, get_list_or_404
from django.db.models import Q
from django.template.context import RequestContext
from consumer.forms import *
from payments.models import *
from django.http import *
from django.core.urlresolvers import reverse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from itertools import tee, chain, izip
from hr.helper import checkDirector, checkReceptionist

def checkCredentials(request):
    if request.user.get_group_permissions()==set([u'meter.add_meterreading']):
        return True

def account_set(applications, active=True, closed=False):
    accounts = []
    for application in [application_set for application_set in applications.filter(account__is_active=active, account__closed=closed)]:
        accounts.extend(list(application.account_set.all()))
    return accounts

def invoice_account_installation(account):
    if account:
        fees = get_list_or_404(Fee, fee_type=Fee.INSTALLATION)
        sum = 0
        invoice = Invoice(account=account)
        invoice.save()
        for charge in fees:
            invoice_detail=InvoiceDetail(fee=charge.fee)
            invoice_detail.save()
            invoice_detail.fee_type = get_object_or_404(Fee, pk=charge.pk)
            invoice_detail.save()
            invoice_detail.total = charge.fee * invoice_detail.quantity
            invoice_detail.invoice_id = invoice
            invoice_detail.save()
            sum += invoice_detail.fee * invoice_detail.quantity
        invoice.total = sum
        invoice.save()  

def previous_and_current(some_iterable):
    if some_iterable:
        prevs, items = tee(some_iterable, 2)
        prevs = chain([None], prevs)
        return izip(prevs, items)
    else:
        return None    
        
@login_required
@csrf_exempt
def consumer(request, pk=None, action=None, cons_type=None, template_name="consumer/consumer_details.html"):
    data = {}
    if cons_type:
        type_id = get_object_or_404(ConsumerType, pk=cons_type)
        ConsumerForm = DomesticConsumerForm if type_id.consumer_type.lower() == 'domestic' else CorporateConsumerForm
    else:
        customer = get_object_or_404(Consumer, pk=pk)
        ConsumerForm = DomesticConsumerForm if customer.consumer_type.consumer_type.lower() == 'domestic' else CorporateConsumerForm
    all_accounts = []
    
    if request.method == "GET":
        if action in ("C", "R", "U"):
            if pk:
                consumer = get_object_or_404(Consumer, pk=pk)
                data['consumer'] = consumer
                data['applications'] = consumer.application_set.all()
                data['unreviewed_applications'] = consumer.application_set.filter(reviewed=False)
                data['active_accounts'] = account_set(data['applications'])
                all_accounts.extend(data['active_accounts'])
                data['inactive_accounts'] = account_set(data['applications'], active=False)
                all_accounts.extend(data['inactive_accounts'])
                data['suspended_accounts'] = account_set(data['applications'], active=False, closed=True)
                all_accounts.extend(data['suspended_accounts'])
                
                #Consumer Financial data
                data['invoices'] =[]
                data['payments'] =[]
                invoice_total = 0
                payment_total = 0
                for account in all_accounts:
                    data['invoices'].extend(list(account.invoice_set.all()))
                for invoice in data['invoices']:
                    invoice_total += invoice.total
                for account in all_accounts:
                    data['payments'].extend(list(account.payment_set.all()))
                for payment in data['payments']:
                    payment_total += payment.amount_paid
                data['invoice_total'] = invoice_total
                data['payment_total'] = payment_total
                data['balance'] = invoice_total-payment_total
                if action in "U":
                    consumerForm = ConsumerForm(instance=get_object_or_404(Consumer, pk=pk))
            else:
                consumerForm = ConsumerForm()
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
                    consumer.consumer_type = get_object_or_404(ConsumerType, pk=cons_type)
                    consumer.save()
                    return HttpResponseRedirect(reverse("application-add", args=[consumer.pk]) if action=="C" else consumer.get_absolute_url())
            else:
                if checkReceptionist(request):
                    return HttpResponseRedirect(reverse("consumer-details", args=[consumer.pk]))
                consumer = get_object_or_404(Consumer, pk=pk)
                consumer.delete()
        else:
            return HttpResponseForbidden()
    if action in ("C","U"):
        if checkDirector(request):
            return HttpResponseRedirect(reverse("consumer-list"))
        data["consumerForm"] = consumerForm
    
    if checkCredentials(request):
        return HttpResponseRedirect(reverse('meter-readings-add'))
    else:
        return render_to_response(template_name, data, context_instance=RequestContext(request))

def consumer_search(request):
    query = request.GET['search']
    data = {'query':query}
    data['consumers'] = Consumer.objects.filter(Q(first_name__icontains=query) | Q(surname__icontains=query) | Q(other_names__icontains=query) | Q(company_name__icontains=query))   
    return render_to_response("consumer/consumer_list.html", data, context_instance=RequestContext(request))

def consumertype_search(request):
    query = request.GET['search']
    data = {'query':query}
    data['consumer_types'] = ConsumerType.objects.filter(consumer_type__icontains=query)
    return render_to_response("consumer/consumer_type_list.html", data, context_instance=RequestContext(request))

def landlord_search(request):
    query = request.GET['search']
    data = {'query':query}
    data['landlords'] = Landlord.objects.filter(Q(first_name__icontains=query) | Q(surname__icontains=query) | Q(other_names__icontains=query) | Q(name_of_company__icontains=query))  
    return render_to_response("consumer/landlords_list.html", data, context_instance=RequestContext(request))

def plot_search(request):
    query = request.GET['search']
    data = {'query':query}
    data['plots'] = Plot.objects.filter(plot_no__icontains=query)
    return render_to_response("consumer/plot_list.html", data, context_instance=RequestContext(request))

@login_required
def consumertype(request, pk=None, action=None, template_name="consumer/consumer_type_form.html"):
    if checkCredentials(request):
        return HttpResponseRedirect(reverse('meter-readings-add'))
    else:
        data = {}
        if request.method == "GET":
            if action in ("create", "read", "update"):
                if pk:
                    data['consumertype'] = get_object_or_404(ConsumerType, pk=pk)
                    rates = data['consumertype'].consumption_set.all()
                    if rates:
                        data['last_rate'] = rates.reverse()[0]
                    data['rates'] = previous_and_current(list(rates))
                    if action == "update":
                        consumertypeForm = ConsumerTypeForm(instance=get_object_or_404(ConsumerType, pk=pk))
                else:
                    consumertypeForm = ConsumerTypeForm()
            else:
                return HttpResponseForbidden()
        elif request.method == "POST":
            if action in ("create", "update"):
                if pk:
                    consumertypeForm = ConsumerTypeForm(request.POST, instance=get_object_or_404(ConsumerType, pk=pk))
                else:
                    consumertypeForm = ConsumerTypeForm(request.POST)
                if consumertypeForm.is_valid():
                    consumertype = consumertypeForm.save(commit=False)
                    consumertype.save()
                    return HttpResponseRedirect(reverse("consumer-type-details", args=[consumertype.pk]))
            else:
                consumertype = get_object_or_404(ConsumerType, pk=pk)
                consumertype.delete()
        if action in ("create", "update"):
            if checkReceptionist(request):
                return HttpResponseRedirect(reverse("consumer-type-list"))
            data['consumertypeForm'] = consumertypeForm
        return render_to_response(template_name, data, context_instance=RequestContext(request))

@login_required
@csrf_exempt
def consumption(request, pk=None, action=None, consumer_type=None, boundary=None, template_name="consumer/consumption_form.html"):
    data = {}
    ConsumptionForm = BoundaryRateForm if boundary != None else NormConsumptionForm
    if request.method == "GET":
        if action in ("create", "read", "update"):
            if pk:
                data['consumption'] = get_object_or_404(Consumption, pk=pk)
                data['consumption_rates'] = previous_and_current(Consumption.objects.filter(consumer_type=data['consumption'].consumer_type))
                if action == "update":
                    consumptionForm = ConsumptionForm(instance=get_object_or_404(Consumption, pk=pk))
            elif consumer_type:
                data['consumertype'] = get_object_or_404(ConsumerType, pk=consumer_type)
                rates = data['consumertype'].consumption_set.all()
                data['consumption_rates'] = previous_and_current(list(rates))
                consumptionForm = ConsumptionForm()
        else:
            return HttpResponseForbidden()
    elif request.method == "POST":
        if action in ("create", "update"):
            if pk:
                consumptionForm = ConsumptionForm(request.POST, instance=get_object_or_404(Consumption, pk=pk))
            else:
                consumptionForm = ConsumptionForm(request.POST)
            if consumptionForm.is_valid():
                if action == "create":
                    rates = Consumption.objects.filter(consumer_type=ConsumerType.objects.filter( pk=consumer_type)).reverse()
                    if rates:
                        rate = rates[0]
                        consumption = consumptionForm.save(commit=False)
                        if rate.border_rate:
                            if rate.max_unit < consumption.max_unit:
                                rate.max_unit = consumption.max_unit +1
                                rate.save()
                        if boundary:
                            consumption.max_unit = rate.max_unit +1 
                            consumption.border_rate = True
                        if consumer_type:
                            consumption.consumer_type = get_object_or_404(ConsumerType, pk=consumer_type)
                        consumption.save()
                    else:
                        consumption = consumptionForm.save(commit=False)
                        if consumer_type:
                            consumption.consumer_type = get_object_or_404(ConsumerType, pk=consumer_type)
                        consumption.save()
                elif action == "update":
                    consumption = consumptionForm.save(commit=False)
                    consumption.save()
                return HttpResponseRedirect(reverse("consumer-type-details", args=[consumption.consumer_type.pk]))
        else:
            consumption = get_object_or_404(Consumption, pk=pk)
            consumption.delete()
    if action in ("create", "update"):
        if checkReceptionist(request):
            return HttpResponseRedirect(reverse("consumer-type-list"))
        data['consumptionForm'] = consumptionForm
    
    if checkCredentials(request):
        return HttpResponseRedirect(reverse('meter-readings-add'))
    else:
        return render_to_response(template_name, data, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def application(request, consumer_pk=None, pk=None, action=None, template_name="consumer/consumer_application.html"):
    data = {}
    if request.method == "GET":
        if action in ("create", "read", "update"):
            if pk:
                data['application'] = get_object_or_404(Application, pk=pk)
                if action == "update":
                    applicationForm = ApplicationForm()
            else:
                data['applicant'] = get_object_or_404(Consumer, pk=consumer_pk)
                applicationForm = ApplicationForm()
        else:
            return HttpResponseForbidden()
    elif request.method == "POST":
        if action in ("create","delete","update"):
            if action in ("create","update"):
                if pk:
                    applicationForm = ApplicationForm(request.POST, instance=get_object_or_404(Application, pk=pk))
                else:
                    applicationForm = ApplicationForm(request.POST)
                if applicationForm.is_valid():
                    application = applicationForm.save(commit=False)
                    application.consumer = get_object_or_404(Consumer, id=consumer_pk)
                    application.save()
                    return HttpResponseRedirect(application.consumer.get_absolute_url())
            else:
                application = get_object_or_404(Application, pk=pk)
                application.delete()
        elif action in ("approve", "reject"):
            application = get_object_or_404(Application, pk=pk)
            application.reviewed = True
            if action == "approve":
                application.approved = True
                account = Account(application=application)
                account.save()
                invoice_account_installation(account)
            else:
                application.approved = False
            application.save()
            return HttpResponseRedirect(application.consumer.get_absolute_url())
    if action in ("create", "update"):
        if action == "create":
            if checkDirector(request):
                return HttpResponseRedirect(reverse("application-list"))
        data['applicationForm'] = applicationForm
    return render_to_response(template_name, data, context_instance=RequestContext(request))

@login_required
def plot(request, pk=None, landlord_id=None, action=None, template_name="consumer/plot_form.html", redirect_field_name = None):
    data = {}
    if request.method == "GET":
        if action in ("create", "read", "update"):
            if pk:
                data['plot'] = get_object_or_404(Plot, pk=pk)
                data['accounts'] = account_set(data['plot'].application_set.filter(reviewed=True, approved=True))
                data['landlord'] = get_object_or_404(Landlord, pk=data['plot'].landlord.id)
                if action == "update":
                    plotForm = PlotForm(instance=get_object_or_404(Plot, pk=pk))
            else:
                plotForm = PlotForm()
                if landlord_id:
                    data['landlord'] = get_object_or_404(Landlord, pk=landlord_id)
                else:
                    landlordForm = LandlordForm()
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
                        landlordForm = LandlordForm()
                else:
                    plot.landlord = get_object_or_404(Landlord, pk=landlord_id)
                plot.save()
                return HttpResponseRedirect(plot.landlord.get_absolute_url())
    if action in ("create", "update"):
        if checkReceptionist(request):
            return HttpResponseRedirect(reverse("consumer-type-list"))
        if checkDirector(request):
            return HttpResponseRedirect(reverse("plot-list"))
        data['plotForm']=plotForm
        if not landlord_id and action=="create":
            data['landlordForm'] = landlordForm
    if checkCredentials(request):
        return HttpResponseRedirect(reverse('meter-readings-add'))
    else:
        return render_to_response(template_name, data, context_instance=RequestContext(request))

@login_required
def landlord (request, pk=None, action=None, template_name="consumer/landlord_form.html"):
    data = {}
    if request.method == "GET":
        if action in ("create", "read", "update"):
            if pk:
                data['landlord'] = get_object_or_404(Landlord, pk=pk)
                data['plots'] = data['landlord'].plot_set.all()
                
                if action == "update":
                    landlordForm = LandlordForm(instance=get_object_or_404(Landlord, pk=pk))
            else:
                landlordForm = LandlordForm()
    elif request.method == "POST":
        if action in ("create", "update"):
            if pk:
                landlordForm = LandlordForm(request.POST, instance=get_object_or_404(Landlord, pk=pk))
            else:
                landlordForm = LandlordForm(request.POST)
            if landlordForm.is_valid():
                landlord = landlordForm.save(commit=False)
                landlord.save()
                return HttpResponseRedirect(landlord.get_absolute_url())
        else:
            landlord = get_object_or_404(Landlord, pk=pk)
            landlord.delete()
    if action in ("create", "update"):
        if checkDirector(request):
                return HttpResponseRedirect(reverse("landlord-list"))
        data['landlordForm'] = landlordForm
    if checkCredentials(request):
        return HttpResponseRedirect(reverse('meter-readings-add'))
    else:
        return render_to_response(template_name, data, context_instance=RequestContext(request))