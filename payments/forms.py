from django import forms
from payments.models import *

class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        
class PaymentModeForm(forms.ModelForm):
    class Meta:
        model = PaymentMode