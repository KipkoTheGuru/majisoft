from django.db import models
from django.contrib import admin
from meter.models import *

class MeterAdmin(admin.ModelAdmin):
    list_display = ["serial_no", "meter_category", "date_purchased", "rent_amount", "reset_value"]

class MeterCategoryAdmin(admin.ModelAdmin):
    list_display = ["meter_category"]

class AccountAdmin(admin.ModelAdmin):
    list_display = ["account_no", "consumer", "zone", "meter_no", "sewer_connected", "is_active", "date_activated"]

class MeterReadingAdmin(admin.ModelAdmin):
    list_display = ["account", "reading", "employee", "reason", "date_recorded"]

class SubZoneAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
        
class ZoneAdmin(admin.ModelAdmin):
    list_display = ["name"]
    
class RegionAdmin(admin.ModelAdmin):
    list_display = ["name"]

class PrevAcctOwnerAdmin(admin.ModelAdmin):
    list_display = ["account_no", "previous_owner", "start_date", "end_date"]
    
admin.site.register(Meter, MeterAdmin)
admin.site.register(MeterCategory, MeterCategoryAdmin)    
admin.site.register(Account, AccountAdmin)
admin.site.register(MeterReading, MeterReadingAdmin)
admin.site.register(SubZone, SubZoneAdmin)
admin.site.register(Zone, ZoneAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(PreviousAccountOwner, PrevAcctOwnerAdmin)
