from django.db import models
from django.contrib import admin
from consumer.models import *

class ConsumerAdmin(admin.ModelAdmin):
    list_display = ["full_name","phone_number", "postal_address", "company_name", "id_number", 
                    "identification_mode","nationality", "nature_of_business","consumer_type"]
    
class TitleAdmin(admin.ModelAdmin):
    list_display = ["name"]

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ["id", "consumer", "landlord", "approved"]
    
class LandlordAdmin(admin.ModelAdmin):
    list_display = ["full_name", "id_number", "identification_mode", "nationality", "name_of_company", "postal_address", 
                    "pin_no", "plot_no", "street"]
    
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["consumer", "feedback_type", "description"]

admin.site.register(Consumer, ConsumerAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Landlord, LandlordAdmin)
admin.site.register(Feedback, FeedbackAdmin)
