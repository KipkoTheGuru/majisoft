# Create your views here.
from consumer.forms import *
from consumer.models import *
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import *
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from meter.models import Account
from meter.forms import AccountForm
from django.views.decorators.csrf import csrf_exempt
import datetime

@csrf_exempt
def account(request, pk=None, action=None, template_name="consumer/consumer_account.html"):
    data = {}
    if request.method == "GET":
        if pk:
            data['account'] = get_object_or_404(Account, pk=pk)
            data["accountForm"] = AccountForm(instance=get_object_or_404(Account, pk=pk))
    if request.method == "POST":
        if action in ("D", "U", "R"):
            if pk:
                if action in ("U", "R"):
                    accountForm = AccountForm(request.POST, instance=get_object_or_404(Account, pk=pk))
                    if accountForm.is_valid():
                        account = accountForm.save(commit=False)
                        today = datetime.datetime.today()
                        account.date_activated = datetime.datetime.today()
                        account.save()
                        return HttpResponseRedirect(reverse("consumer-details", args=[account.application.consumer.pk]))
                    else:
                        pass
                if action == "D":
                    pass
        elif action in ("activate", "close"):
            account = get_object_or_404(Account, pk=pk)
            if action == "activate":
                account.closed = False
                account.is_active = True
            elif action=="close":
                account.closed = True
                account.is_active = False
            account.save()
    return render_to_response(template_name, data, context_instance=RequestContext(request))
