from django import forms
from .models import Code


# class SymptomAppointmentForm(forms.Form):
#     Dept = forms.CharField()

class CodeForm(forms.ModelForm):
    number = forms.CharField(label='OTP Code', help_text='Enter OTP HERE.')
    class Meta: 
        model = Code 
        fields = ('number',)