from django import forms
from consumer.models import *

class DomesticConsumerForm(forms.ModelForm):
    class Meta:
        model = Consumer
        exclude = ["nature_of_business", "company_name", "landline_no", "consumer_type"]

class CorporateConsumerForm(forms.ModelForm):
    first_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    other_names = models.CharField(max_length=50, blank=True, null = True)
    company_name = forms.CharField(max_length=50)
    nature_of_business = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Consumer
        exclude = ["consumer_type"]        

class ConsumerTypeForm(forms.ModelForm):
    class Meta:
        model = ConsumerType 

class NormConsumptionForm(forms.ModelForm):
    class Meta:
        model = Consumption
        exclude = ["consumer_type", "border_rate"]
        
class BoundaryRateForm(forms.ModelForm):
    class Meta:
        model = Consumption
        exclude = ["consumer_type", "border_rate", "max_unit"]
        
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        exclude = ["consumer", "reviewed", "approved"]
        
class PlotForm(forms.ModelForm):
    class Meta:
        model = Plot
        exclude = ['landlord']

class LandlordForm(forms.ModelForm):
    class Meta:
        model = Landlord
        
class TitleForm(forms.ModelForm):
    class Meta:
        model = Title
        
class TitleForm(forms.ModelForm):
    class Meta:
        model = Title
        
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback