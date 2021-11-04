from django import forms
from django.contrib.auth.models import User
from .models import Washer_Profile,Washing_Order
from django.core import validators
from django.contrib import messages


class WasherProfileForm(forms.ModelForm):
    class Meta():
        model = Washer_Profile
        fields = ('washer_name','washer_location')


class WashOrderForm(forms.ModelForm):
    class Meta():
        model = Washing_Order
        fields = ('customer_name','car_model')

    # def __init__(self, *args, **kwargs):
    #     super(WashOrderForm, self).__init__(*args, **kwargs)
    #     self.fields['assigned_to']=forms.ModelChoiceField(queryset=Washer_Profile.objects.exclude(is_available=False))
     
        


