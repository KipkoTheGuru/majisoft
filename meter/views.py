# Create your views here.
from consumer.forms import *
from consumer.models import *
from django.core import serializers
from django.http import *
from django.shortcuts import get_object_or_404, render_to_response, get_list_or_404
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from meter.models import *
from payments.models import *
from meter.forms import *
from django.views.decorators.csrf import csrf_exempt
from config.settings import *
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from hr.helper import checkCredentials, checkDirector, checkReceptionist

READINGS_DUMP_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../readings-dump/readings.txt')
)

def region_search(request):
    query = request.GET['search']
    data = {'query':query}
    data['regions'] = Region.objects.filter(name__icontains=query)
    return render_to_response("meter/region_list.html", data, context_instance=RequestContext(request))

def zone_search(request):
    query = request.GET['search']
    data = {'query':query}
    data['zones'] = Zone.objects.filter(name__icontains=query)
    return render_to_response("meter/zone_list.html", data, context_instance=RequestContext(request))

def subzone_search(request):
    query = request.GET['search']
    data = {'query':query}
    data['subzones'] = SubZone.objects.filter(name__icontains=query)
    return render_to_response("meter/subzone_list.html", data, context_instance=RequestContext(request))

@login_required
@csrf_exempt
def account(request, pk=None, action=None, template_name="consumer/consumer_account.html"):
    data = {}
    if request.method == "GET":
        if pk:
            data['account'] = get_object_or_404(Account, pk=pk)
            accountForm = AccountForm(instance=get_object_or_404(Account, pk=pk))
    if request.method == "POST":
        if action in ("C","U", "R"):
            if action in ("U", "R"):
                if checkDirector(request):
                    return HttpResponseRedirect(reverse("account-list"))
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
                account.date_activated = datetime.datetime.today()
            elif action=="close":
                account.closed = True
                account.is_active = False
                account.date_closed = datetime.datetime.today()
            account.save()
    if action in ("C","U", "R"):
        if action in ("U", "R"):
            if checkDirector(request):
                return HttpResponseRedirect(reverse("account-list"))
        if action in ("C", "U"):
            if checkReceptionist(request):
                return HttpResponseRedirect(reverse("account-list"))
        data["accountForm"] = accountForm
    if checkCredentials(request):
        return HttpResponseRedirect(reverse('meter-readings-add'))
    else:
        return render_to_response(template_name, data, context_instance=RequestContext(request))

@login_required
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
                if checkReceptionist(request):
                    return HttpResponseRedirect(reverse("subzone-list"))
                subzone = get_object_or_404(SubZone, pk=pk)
                if zone_pk:
                    subzone.zone = get_object_or_404(Zone, id=region_pk)
                subzone.delete()
    if action in ("C", "U"):
        if checkReceptionist(request):
            return HttpResponseRedirect(reverse("subzone-list"))
        if checkDirector(request):
            return HttpResponseRedirect(reverse("subzone-list"))
        data['subzoneForm'] = subzoneForm
        data['locationForm'] = subzoneForm
    if checkCredentials(request):
        return HttpResponseRedirect(reverse('meter-readings-add'))
    else:
        return render_to_response(template_name, data, context_instance=RequestContext(request))

@login_required
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
                if checkReceptionist(request):
                    return HttpResponseRedirect(reverse("subzone-list"))
                zone = get_object_or_404(Zone, pk=pk)
                zone.delete()
    if action in ("C", "U"):
        if checkReceptionist(request):
            return HttpResponseRedirect(reverse("zone-list"))
        if checkDirector(request):
            return HttpResponseRedirect(reverse("zone-list"))
        data['zoneForm'] = zoneForm
        data['locationForm'] = zoneForm
    if checkCredentials(request):
        return HttpResponseRedirect(reverse('meter-readings-add'))
    else:
        return render_to_response(template_name, data, context_instance=RequestContext(request))

@login_required
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
                if checkReceptionist(request):
                    return HttpResponseRedirect(reverse("subzone-list"))
                region = get_object_or_404(Region, pk=pk)
                region.delete()
    if action in ("C", "U"):
        if checkReceptionist(request):
            return HttpResponseRedirect(reverse("subzone-list"))
        if checkDirector(request):
            return HttpResponseRedirect(reverse("region-list"))
        data['regionForm'] = regionForm
        data['locationForm'] = regionForm
    if checkCredentials(request):
        return HttpResponseRedirect(reverse('meter-readings-add'))
    else:
        return render_to_response(template_name, data, context_instance=RequestContext(request))

@login_required
def meter_readings(request, pk=None, action=None, template_name="meter/upload_readings.html"):
    data = {}
    if request.method == "GET":
        if action == 'C':
            form = MeterReadingsForm()
    if request.method == 'POST':
        form = MeterReadingsForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['meter_readings_file'])
            data = upload_readings(request.user.pk)
            form = MeterReadingsForm()
            #return HttpResponseRedirect(reverse("uploaded-readings"))
        else:
            form = MeterReadingsForm()
    if action == 'C':
        if checkReceptionist(request):
            return HttpResponseRedirect(reverse("subzone-list"))
        if checkDirector(request):
            return HttpResponseRedirect(reverse("home"))
        data['form'] = form
    return render_to_response(template_name, data, context_instance=RequestContext(request))

def handle_uploaded_file(f):
    destination = open(READINGS_DUMP_FOLDER, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

def upload_readings(user_id):
    a = open(READINGS_DUMP_FOLDER, 'r')
    readingslist = a.readlines()
    accounts=[]
    new_readings=[]
    info_to_display = {'errors':[], 'info':[]}
    for reading in readingslist:
        meter_no, meter_reading=reading.split('\t')
        try:
            account = Account.objects.get(meter_no=Meter.objects.get(serial_no=meter_no), is_active = True)
            if account:
                new_reading = MeterReading.objects.create(account=account, reading=meter_reading, employee = get_object_or_404(User, pk = user_id))
                accounts.append(account)
                new_readings.append(new_reading.reading)
                info_to_display['info'].append("Account no %s had a reading of %s " % (account.account_no, new_reading))
        except ObjectDoesNotExist:
            info_to_display['errors'].append("The account with meter no %s does not exist or is not active" % meter_no)
    invoice_account(accounts,new_readings)
    return info_to_display
    
def invoice_account(accounts, new_readings):
    if accounts and new_readings:
        for account, new_reading in zip(accounts, new_readings):
            perform_calculations(account, new_reading)

def perform_calculations(account, new_reading):
    prev_reading = MeterReading.objects.filter(account=account).reverse()[:2]
    total_consumption = 0
    #Calculating total consumption since previous reading
    if prev_reading != None:
        total_consumption = int(new_reading) - prev_reading[0].reading
    total = 0
    water_rate = 0
    sewerage_rate = 0
    #Calculating the total to be charged on the invoice
    tariffs = Consumption.objects.filter(consumer_type=account.application.consumer.consumer_type).reverse()
    if total_consumption > tariffs[0].max_unit:
        total = (total_consumption * tariffs[0].water)
        if account.sewer_connected:
            total += total_consumption*tariffs[0].sewerage
    else:
        for tariff in tariffs:
            if total_consumption < tariff.max_unit:
                water_rate = tariff.water
                total = (total_consumption * tariff.water)
                if account.sewer_connected:
                    total += tariff.sewerage
                    sewerage_rate = tariff.sewerage
                break
    invoice = Invoice(account=account)
    invoice.save()
    invoice_detail=InvoiceDetail.objects.create(fee=water_rate, quantity = total_consumption, total=total_consumption * tariff.water, invoice_id=invoice)
    if sewerage_rate:
        invoice_detail=InvoiceDetail.objects.create(fee=sewerage_rate, quantity = 1, total=total_consumption * tariff.water, invoice_id=invoice)
    invoice.total = total
    invoice.save()
    