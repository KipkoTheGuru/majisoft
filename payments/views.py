# Create your views here.
from consumer.models import *
from payments.models import *
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.template.context import RequestContext
from payments.forms import *
from django.http import *
from django.core.urlresolvers import reverse
from django.core import serializers

@login_required
def fee(request, pk=None, action=None, template_name="payments/fee_form.html"):
    data = {}
    if request.method == "GET":
        if action in ("create", "read", "update"):
            if pk:
                data['fee'] = get_object_or_404(Fee, pk=pk)
                if action == "update":
                    feeForm = FeeForm(instance=get_object_or_404(Fee, pk=pk))
            else:
                feeForm = FeeForm()
    elif request.method == "POST":
        if action in ("create", "update"):
            if pk:
                feeForm = FeeForm(request.POST, instance=get_object_or_404(Fee, pk=pk))
            else:
                feeForm = FeeForm(request.POST)
            if feeForm.is_valid():
                fee = feeForm.save(commit=False)
                fee.save()
                return HttpResponseRedirect(reverse("fee-details", args=[fee.pk]))
        else:
            fee = get_object_or_404(Fee, pk=pk)
            fee.delete()
    if action in ("create", "update"):
        data['feeForm'] = feeForm
    return render_to_response(template_name, data, context_instance=RequestContext(request))

@login_required
def payment_mode (request, pk=None, action=None, template_name="payments/payment_mode_form.html"):
    data = {}
    if request.method == "GET":
        if action in ("create", "read", "update"):
            if pk:
                data['paymentMode'] = get_object_or_404(PaymentMode, pk=pk)
                if action == "update":
                    paymentModeForm = PaymentModeForm(instance=get_object_or_404(PaymentMode, pk=pk))
            else:
                paymentModeForm = PaymentModeForm()
    elif request.method == "POST":
        if action in ("create", "update"):
            if pk:
                paymentModeForm = PaymentModeForm(request.POST, instance=get_object_or_404(PaymentMode, pk=pk))
            else:
                paymentModeForm = PaymentModeForm(request.POST)
            if paymentModeForm.is_valid():
                paymentMode = paymentModeForm.save(commit=False)
                paymentMode.save()
                return HttpResponseRedirect(reverse("payment-mode-details", args=[paymentMode.pk]))
        else:
            paymentMode = get_object_or_404(PaymentMode, pk=pk)
            paymentMode.delete()
    if action in ("create", "update"):
        data['paymentModeForm'] = paymentModeForm
    return render_to_response(template_name, data, context_instance=RequestContext(request))

@login_required
def payment(request, pk=None, action=None, template_name="payments/payment_form.html"):
    data = {}
    if request.method == "GET":
        if action in ("create", "read", "update"):
            data['payment'] = get_object_or_404(PaymentMode, pk=pk)