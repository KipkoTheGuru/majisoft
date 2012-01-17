from django import forms
from consumer.models import *

class DomesticConsumerForm(forms.ModelForm):
    class Meta:
        model = Consumer
        exclude = ["nature_of_business", "company_name", "landline_no", "consumer_type"]

class CorporateConsumerForm(forms.ModelForm):
    class Meta:
        model = Consumer
        exclude = ["consumer_type"]        

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