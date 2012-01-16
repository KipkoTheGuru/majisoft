from django.db import models
from django.contrib import admin
from meter.models import *

class MeterAdmin(admin.ModelAdmin):
    list_display = ["serial_no", "meter_category", "date_purchased", "reset_value"]
    search_fields = ["serial_no"]

class MeterCategoryAdmin(admin.ModelAdmin):
    list_display = ["measure", "thickness", "rent_amount"]
    search_fields = ["diameter"]

class AccountAdmin(admin.ModelAdmin):
    list_display = ["account_no", "application", "meter_no", "sewer_connected", "is_active", "date_activated"]
    search_fields = ["consumer", "sub_zone"]

class MeterReadingAdmin(admin.ModelAdmin):
    list_display = ["account", "reading", "employee", "reason", "date_recorded"]
    search_fields = ["account"]
    list_filter = ['date_recorded']

class SubZoneAdmin(admin.ModelAdmin):
    list_display = ["name", "zone", "description"]
    search_fields = ["name"]
        
class ZoneAdmin(admin.ModelAdmin):
    list_display = ["name", "region"]
    search_fields = ["name"]
    
class RegionAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]

class PrevAcctOwnerAdmin(admin.ModelAdmin):
    list_display = ["account_no", "previous_owner", "start_date", "end_date"]
    search_fields = ["account_no"]
    
admin.site.register(Meter, MeterAdmin)
admin.site.register(MeterCategory, MeterCategoryAdmin)    
admin.site.register(Account, AccountAdmin)
admin.site.register(MeterReading, MeterReadingAdmin)
admin.site.register(SubZone, SubZoneAdmin)
admin.site.register(Zone, ZoneAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(PreviousAccountOwner, PrevAcctOwnerAdmin)
