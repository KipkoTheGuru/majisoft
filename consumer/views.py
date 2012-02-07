# Create your views here.
from consumer.models import *
from meter.models import Account
from django.shortcuts import get_object_or_404, render_to_response, get_list_or_404
from django.db.models import Sum
from django.template.context import RequestContext
from consumer.forms import *
from payments.models import *
from django.http import *
from django.core.urlresolvers import reverse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

def account_set(applications, active=True, closed=False):
    accounts = []
    for application in [application_set for application_set in applications.filter(account__is_active=active, account__closed=closed)]:
        accounts.extend(list(application.account_set.all()))
    return accounts

def set_max_boundary_consumption():
    pass

def invoice_account_installation(account):
    if account:
        fees = get_list_or_404(Fee, fee_type=Fee.INSTALLATION)
        sum = 0
        invoice = Invoice(account=account)
        invoice.save()
        for charge in fees:
            invoice_detail=InvoiceDetail(fee=charge.fee)
            invoice_detail.save()
            invoice_detail.total = charge.fee * invoice_detail.quantity
            invoice_detail.invoice_id = invoice
            invoice_detail.save()
            sum += invoice_detail.fee * invoice_detail.quantity
        invoice.total = sum
        invoice.save()

def get_financial_history(invoices, payments):
    if invoices.__len__() > payments.__len__():
        x = invoices.__len__()
    else:
        x = payments.__len__()
    financial_history = []
    for i in range(x, 0, -1):
        pass
         

@csrf_exempt
def consumer(request, pk=None, action=None, consumer_type='domestic', template_name="consumer/consumer_details.html"):
    data = {}
    all_accounts = []
    ConsumerForm = DomesticConsumerForm if consumer_type.lower() == 'domestic' else CorporateConsumerForm
    data['consumer_type'] = consumer_type
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
                payments=[]
                invoice_total = 0
                payment_total = 0
                for account in all_accounts:
                    data['invoices'].extend(list(account.invoice_set.all()))
                for invoice in data['invoices']:
                    invoice_total += invoice.total
                for invoice in data['invoices']:
                    payments.extend(list(invoice.payment_set.all()))
                for payment in payments:
                    payment_total += payment.amount_paid
                data['balance'] = payment_total - invoice_total
                if action in "U":
                    consumerForm = ConsumerForm(instance=get_object_or_404(Consumer, pk=pk))
            else:
                data['consumer_type'] = consumer_type
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
                    consumer.consumer_type = get_object_or_404(ConsumerType, consumer_type__iexact=consumer_type)
                    consumer.save()
                    return HttpResponseRedirect(reverse("application-add", args=[consumer.pk]) if action=="C" else consumer.get_absolute_url())
            else:
                consumer = get_object_or_404(Consumer, pk=pk)
                consumer.delete()
        else:
            return HttpResponseForbidden()
    if action in ("C","U"):
        data["consumerForm"] = consumerForm
    return render_to_response(template_name, data, context_instance=RequestContext(request))

def consumertype(request, pk=None, action=None, template_name="consumer/consumer_type_form.html"):
    data = {}
    if request.method == "GET":
        if action in ("create", "read", "update"):
            if pk:
                data['consumertype'] = get_object_or_404(ConsumerType, pk=pk)
                data['rates'] = data['consumertype'].consumption_set.all()
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
        data['consumertypeForm'] = consumertypeForm
    return render_to_response(template_name, data, context_instance=RequestContext(request))

@csrf_exempt
def consumption(request, pk=None, action=None, consumer_type=None, template_name="consumer/consumption_form.html"):
    data = {}
    if request.method == "GET":
        if action in ("create", "read", "update"):
            if pk:
                data['consumption'] = get_object_or_404(Consumption, pk=pk)
                if action == "update":
                    consumptionForm = ConsumptionForm(instance=get_object_or_404(Consumption, pk=pk))
            elif consumer_type:
                data['consumertype'] = get_object_or_404(ConsumerType, pk=consumer_type)
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
                consumption = consumptionForm.save(commit=False)
                if consumer_type:
                    consumption.consumer_type = get_object_or_404(ConsumerType, pk=consumer_type)
                consumption.save()
                return HttpResponseRedirect(reverse("consumer-type-details", args=[consumption.consumer_type.pk]))
        else:
            consumption = get_object_or_404(Consumption, pk=pk)
            consumption.delete()
    if action in ("create", "update"):
        data['consumptionForm'] = consumptionForm
    return render_to_response(template_name, data, context_instance=RequestContext(request))

@csrf_exempt
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
        data['applicationForm'] = applicationForm
    return render_to_response(template_name, data, context_instance=RequestContext(request))

def plot(request, pk=None, landlord_id=None, action=None, template_name="consumer/plot_form.html"):
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
        data['plotForm']=plotForm
        if not landlord_id and action=="create":
            data['landlordForm'] = landlordForm
    return render_to_response(template_name, data, context_instance=RequestContext(request))

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
        data['landlordForm'] = landlordForm
    return render_to_response(template_name, data, context_instance=RequestContext(request))