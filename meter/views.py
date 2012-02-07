# Create your views here.
from consumer.forms import *
from consumer.models import *
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import *
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from meter.models import *
from meter.forms import *
from django.views.decorators.csrf import csrf_exempt
import datetime

@csrf_exempt
def account(request, pk=None, action=None, template_name="consumer/consumer_account.html"):
    data = {}
    if request.method == "GET":
        if pk:
            data['account'] = get_object_or_404(Account, pk=pk)
            accountForm = AccountForm(instance=get_object_or_404(Account, pk=pk))
    if request.method == "POST":
        if action in ("C","U", "R"):
            if pk:
                accountForm = AccountForm(request.POST, instance=get_object_or_404(Account, pk=pk))
            else:
                accountForm = AccountForm(request.POST)
            if accountForm.is_valid():
                account = accountForm.save(commit=False)
                account.date_activated = datetime.datetime.today()
                account.save()
                return HttpResponseRedirect(reverse("consumer-details", args=[account.application.consumer.pk]))
        elif action in ("activate", "close"):
            account = get_object_or_404(Account, pk=pk)
            if action == "activate":
                account.closed = False
                account.is_active = True
            elif action=="close":
                account.closed = True
                account.is_active = False
                account.date_closed = datetime.datetime.today()
            account.save()
    if action in ("C","U", "R"):
        data["accountForm"] = accountForm
    return render_to_response(template_name, data, context_instance=RequestContext(request))

def subzone(request, pk=None, zone_pk=None, action=None, template_name="meter/location_form.html"):
    data = {}
    SubZoneForm = SubZoneConForm if zone_pk else SubZoneSinForm
    if request.method == "GET":
        if action in ("C", "U", "R"):
            if pk:
                data['subzone'] = get_object_or_404(SubZone, pk=pk)
                data['plots'] = data['subzone'].plot_set.all()
                if action == "U":
                    subzoneForm = SubZoneForm(instance=get_object_or_404(SubZone, pk=pk))
            else:
                subzoneForm = SubZoneForm()
    if request.method == "POST":
        if action in ("C", "U", "D"):
            if action in ("C", "U"):
                if pk:
                    subzoneForm = SubZoneForm(request.POST, instance=get_object_or_404(SubZone, pk=pk))
                else:
                    subzoneForm = SubZoneForm(request.POST)
                if subzoneForm.is_valid():
                    subzone = subzoneForm.save(commit=False)
                    subzone.save()
                    return HttpResponseRedirect(reverse("subzone-details", args=[subzone.pk]))
            else:
                subzone = get_object_or_404(SubZone, pk=pk)
                if zone_pk:
                        subzone.zone = get_object_or_404(Zone, id=region_pk)
                subzone.delete()
    if action in ("C", "U"):
        data['subzoneForm'] = subzoneForm
        data['locationForm'] = subzoneForm
    return render_to_response(template_name, data, context_instance=RequestContext(request))

def zone(request, pk=None, region_pk=None, action=None, template_name="meter/location_form.html"):
    data = {}
    ZoneForm = ZoneConRegionForm if region_pk else ZoneSinRegionForm
    if request.method == "GET":
        if action in ("C", "U", "R"):
            if pk:
                data['zone'] = get_object_or_404(Zone, pk=pk)
                data['subzones'] = data['zone'].subzone_set.all()
                if action == "U":
                    zoneForm = ZoneForm(instance=get_object_or_404(Zone, pk=pk))
            else:
                zoneForm = ZoneForm()
    if request.method == "POST":
        if action in ("C", "U", "D"):
            if action in ("C", "U"):
                if pk:
                    zoneForm = ZoneForm(request.POST, instance=get_object_or_404(Zone, pk=pk))
                else:
                    zoneForm = ZoneForm(request.POST)
                if zoneForm.is_valid():
                    zone = zoneForm.save(commit=False)
                    if region_pk:
                        zone.region = get_object_or_404(Region, id=region_pk)
                    zone.save()
                    return HttpResponseRedirect(reverse("zone-details", args=[zone.pk]))
            else:
                zone = get_object_or_404(Zone, pk=pk)
                zone.delete()
    if action in ("C", "U"):
        data['zoneForm'] = zoneForm
        data['locationForm'] = zoneForm
    return render_to_response(template_name, data, context_instance=RequestContext(request))

def region(request, pk=None, action=None, template_name="meter/location_form.html"):
    data = {}
    if request.method == "GET":
        if action in ("C", "U", "R"):
            if pk:
                data['region'] = get_object_or_404(Region, pk=pk)
                data['zones'] = data['region'].zone_set.all()
                if action == "U":
                    regionForm = RegionForm(instance=get_object_or_404(Region, pk=pk))
            else:
                regionForm = RegionForm()
    if request.method == "POST":
        if action in ("C", "U", "D"):
            if action in ("C", "U"):
                if pk:
                    regionForm = RegionForm(request.POST, instance=get_object_or_404(Region, pk=pk))
                else:
                    regionForm = RegionForm(request.POST)
                if regionForm.is_valid():
                    region= regionForm.save(commit=False)
                    region.save()
                    return HttpResponseRedirect(reverse("region-details", args=[region.pk]))
            else:
                region = get_object_or_404(Region, pk=pk)
                region.delete()
    if action in ("C", "U"):
        data['regionForm'] = regionForm
        data['locationForm'] = regionForm
    return render_to_response(template_name, data, context_instance=RequestContext(request))