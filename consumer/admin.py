from django.db import models
from django.contrib import admin
from consumer.models import *

class ConsumerAdmin(admin.ModelAdmin):
    list_display = ["full_name", "mobile_no", "landline_no", "full_address", "company_name", "id_number", "pin_no",
                    "nationality", "consumer_type", "date_registered"]
    search_fields = ['full_name', "mobile_no", "landline_no", "id_number", "pin_no"]
    
class ConsumerTypeAdmin(admin.ModelAdmin):
    list_display = ["consumer_type"]
    search_fields = ["consumer_type"]
    
class TitleAdmin(admin.ModelAdmin):
    list_display = ["name"]

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ["id", "consumer", "plot_no", "approved", "reviewed"]
    search_fields = ["consumer"]

class PlotAdmin(admin.ModelAdmin):
    list_display = ["plot_no", "landlord", "sub_zone", "street"]
    search_fields = ["plot_no", "landlord"]
    
class LandlordAdmin(admin.ModelAdmin):
    list_display = ["full_name", "id_number", "nationality", "name_of_company","pin_no", "full_address"]
    search_fields = ['full_name', "mobile_no", "id_number", "pin_no"]
    
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["consumer", "feedback_type", "description"]
    search_fields = ["consumer"]

admin.site.register(Consumer, ConsumerAdmin)
admin.site.register(ConsumerType, ConsumerTypeAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Plot, PlotAdmin)
admin.site.register(Landlord, LandlordAdmin)
admin.site.register(Feedback, FeedbackAdmin)
