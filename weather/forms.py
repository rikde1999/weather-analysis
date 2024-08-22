# weather/forms.py
from django import forms


class CityForm(forms.Form):
    city = forms.CharField(max_length=100, required=False, help_text="Enter city name")
