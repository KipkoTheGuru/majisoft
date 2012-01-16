from django import forms
from meter.models import *

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ["date_activated", "closed", "application"]