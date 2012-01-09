from django import forms
from consumer.models import *

class DomesticConsumerForm(forms.ModelForm):
    class Meta:
        model = Consumer
        exclude = ["nature_of_business", "company_name", "landline_no"]

class CorporateConsumerForm(forms.ModelForm):
    first_name = models.CharField("Director's First Name", max_length=50)
    surname = models.CharField("Director's Surname", max_length=50)
    other_names = models.CharField("Director's Other Names", max_length=50, blank=True, null = True)
    mobile_no = models.CharField("Director's Mobile No", max_length=50)
    id_number = models.CharField("Director's National ID/Passport No", max_length=50, unique=True)
    pin_no = models.CharField("Director's PIN No", max_length=50)
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