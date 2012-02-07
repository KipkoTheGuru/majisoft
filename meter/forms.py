from django import forms
from meter.models import *

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ["date_activated", "closed", "application"]
        
class MeterCategoryForm(forms.ModelForm):
    class Meta:
        model = MeterCategory
        
class MeterForm(forms.ModelForm):
    class Meta:
        model = Meter

class MeterReadingForm(forms.ModelForm):
    class Meta:
        model = MeterReading
        exclude = ["employee", "date_recorded"]

class SubZoneConForm(forms.ModelForm):
    class Meta:
        model = SubZone
        exclude = ["zone"]

class SubZoneSinForm(forms.ModelForm):
    class Meta:
        model = SubZone

class ZoneConRegionForm(forms.ModelForm):
    class Meta:
        model = Zone
        exclude = ["region"]
        
class ZoneSinRegionForm(forms.ModelForm):
    class Meta:
        model = Zone

class RegionForm(forms.ModelForm):
    class Meta:
        model = Region