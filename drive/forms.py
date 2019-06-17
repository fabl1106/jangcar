from django import forms
from .models import Drive
from django.contrib.auth.models import User

class DriveRegisterForm(forms.ModelForm):
    class Meta:
        model = Drive
        fields = ['departure_area','arrive_area','departure_date','departure_time','detail_plan','fee','memo']
