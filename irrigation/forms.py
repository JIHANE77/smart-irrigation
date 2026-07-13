from django import forms
from .models import Parcelle, Culture, Meteo

class ParcelleForm(forms.ModelForm):
    class Meta:
        model = Parcelle
        fields = '__all__'

class CultureForm(forms.ModelForm):
    class Meta:
        model = Culture
        fields = '__all__'
class MeteoForm(forms.ModelForm):
    class Meta:
        model = Meteo
        fields = '__all__'