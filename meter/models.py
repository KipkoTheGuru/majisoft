from django.db import models
from django.contrib.auth.models import User
from consumer.models import Consumer, Application
from hr.models import Employee

class Meter(models.Model):
    METER_STATUS=(
         (1, "Working"),
         (2, "Damaged")
     )
    serial_no = models.CharField(max_length=30, unique=True)
    meter_category = models.ForeignKey("MeterCategory", verbose_name='Meter Category(in mm)')
    meter_status = models.IntegerField(choices=METER_STATUS)
    date_purchased = models.DateField()
    reset_value = models.IntegerField(default=10000)
    
    class Meta:
        db_table = "Meter"
        
    def __unicode__(self):
        return "%s" % self.serial_no

class MeterCategory(models.Model):
    measure = models.IntegerField(unique=True, verbose_name='Measure(in mm)')
    thickness = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Thickness(in inches)')
    rent_amount = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Rent (Ksh)')
    
    class Meta:
        db_table = "MeterCategory"
        verbose_name_plural = "Meter Categories"
    
    def __unicode__(self):
        return "%d mm" % self.measure

class Account(models.Model):
    meter_no = models.ForeignKey(Meter, blank=True, null=True)
    application = models.ForeignKey(Application)
    sewer_connected = models.BooleanField(default=False)
    refuse = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    date_activated = models.DateTimeField("Last Activated On", editable=False, blank=True, null=True)
    date_closed = models.DateTimeField("Closed On", editable=False, blank=True, null=True)
    
    class Meta:
        db_table = "Account"
    
    def __unicode__(self):
        return "%s" % (self.account_no)
    
    @property
    def account_no(self):
        return "%d-%d%d" % (self.application.consumer.pk, self.id, self.application.plot_no.sub_zone.pk)
    

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

class SubZone(models.Model):
    name = models.CharField(max_length=50, unique=True)
    zone = models.ForeignKey("Zone")
    description = models.TextField(max_length=500)
    
    class Meta:
        db_table = "SubZone"
    
    def __unicode__(self):
        return "%s" % (self.name)
        
class Zone(models.Model):
    name = models.CharField(max_length=50, unique=True)
    region = models.ForeignKey("Region")
    
    class Meta:
        db_table = "Zone"
    
    def __unicode__(self):
        return "%s" % (self.name)
    
class Region(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    class Meta:
        db_table = "Region"
    
    def __unicode__(self):
        return "%s" % (self.name)
    
    