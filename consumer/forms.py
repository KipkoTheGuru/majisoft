from django import forms
from consumer.models import *

class DomesticConsumerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ConsumerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Consumer
        exclude = ["nature_of_business", "company_name", "landline_no"]

class CorporateConsumerForm(forms.ModelForm):
    class Meta:
        model = Consumer        

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        
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