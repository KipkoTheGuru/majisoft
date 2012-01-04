from django.db import models
from django.contrib import admin
from hr.models import *

class EmployeeAdmin(admin.ModelAdmin):    
    def groups(self, employee):
        return ", ".join([group.name for group in employee.user.groups.filter()])
    
    list_display = ["full_name", "phone_number", "national_id", "groups"]
    
admin.site.register(Employee, EmployeeAdmin)
