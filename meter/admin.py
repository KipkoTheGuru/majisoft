from django.db import models
from django.contrib import admin
from meter.models import *

class MeterAdmin(admin.ModelAdmin):
    list_display = ["serial_no"]

class AccountAdmin(admin.ModelAdmin):
    list_display = ["account_no", "consumer", "zone", "meter_no", "sewer_connected", "is_active", "date_activated"]

class MeterReadingAdmin(admin.ModelAdmin):
    list_display = ["account", "reading", "employee", "reason", "date_recorded"]
        
class ZoneAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]

class PrevAcctOwnerAdmin(admin.ModelAdmin):
    list_display = ["account_no", "previous_owner", "start_date", "end_date"]
    
admin.site.register(Meter, MeterAdmin)    
admin.site.register(Account, AccountAdmin)
admin.site.register(MeterReading, MeterReadingAdmin)
admin.site.register(Zone, ZoneAdmin)
admin.site.register(PreviousAccountOwner, PrevAcctOwnerAdmin)
