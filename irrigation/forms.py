from django import forms
from .models import Parcelle, Culture

class ParcelleForm(forms.ModelForm):
    class Meta:
        model = Parcelle
        fields = '__all__'

class CultureForm(forms.ModelForm):
    class Meta:
        model = Culture
        fields = '__all__'