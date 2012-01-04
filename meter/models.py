from django.db import models
from django.contrib.auth.models import User
from consumer.models import Consumer
from hr.models import Employee

class Meter(models.Model):
    serial_no = models.CharField(max_length=30)
    
    class Meta:
        db_table = "Meter"

class Account(models.Model):
    account_no = models.CharField(max_length=50)
    zone = models.ForeignKey("Zone")
    consumer = models.ForeignKey(Consumer)
    meter_no = models.ForeignKey(Meter)
    service_line_diameter = models.DecimalField(max_digits=10, decimal_places=3)
    sewer_connected = models.BooleanField(default=False)
    refuse = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_activated = models.DateTimeField("Last Date Activated")
    
    class Meta:
        db_table = "Account"
    
    def __unicode__(self):
        return "%s" % (self.account_no)

class PreviousAccountOwner(models.Model):
    account_no = models.ForeignKey("Account")
    previous_owner = models.ForeignKey(Consumer)
    start_date = models.DateTimeField("Last Date Activated")
    end_date = models.DateTimeField("Last Date Activated", blank=True, null=True)
    
    class Meta:
        db_table = "PreviousOwner"

class MeterReading(models.Model):
    account = models.ForeignKey(Account)
    reading = models.CharField(max_length=50)
    employee = models.ForeignKey(Employee, verbose_name="Submitted by")
    reason = models.CharField(max_length=200, blank=True, null=True)
    date_recorded = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "MeterReading"
        
class Zone(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    
    class Meta:
        db_table = "Zone"
    
    def __unicode__(self):
        return "%s" % (self.name)
        