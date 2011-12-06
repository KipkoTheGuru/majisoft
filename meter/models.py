from django.db import models
from django.contrib.auth.models import User
from consumer.models import Consumer
from hr.models import Employee

class Account(models.Model):
    account_no = models.CharField(max_length=50)
    consumer = models.ForeignKey(Consumer)
    zone = models.ForeignKey("Zone")
    meter_no = models.CharField(max_length=50)
    meter_serial_no = models.CharField(max_length=50)
    sewer_connected = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_activated = models.DateTimeField("Last Date Activated", auto_now_add=True)
    
    class Meta:
        db_table = "Account"
    
    def __unicode__(self):
        return "%s" % (self.account_no)

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
        return "%s, %s" % (self.name, self.description)
        