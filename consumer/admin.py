from django.db import models
from django.contrib import admin
from consumer.models import *

class ConsumerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "sur_name"]
    
class TitleAdmin(admin.ModelAdmin):
    list_display = ["name"]

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ["consumer", "landlord", "approved"]
    
class LandlordAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "sur_name"]
    
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["consumer", "feedback_type"]

admin.site.register(Consumer, ConsumerAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Landlord, LandlordAdmin)
admin.site.register(Feedback, FeedbackAdmin)
